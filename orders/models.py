from datetime import date, timedelta
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from pulp import LpProblem, LpVariable, LpMaximize, lpSum

from baskets.utils import get_beginning_of_week
from baskets.models import Basket, BasketPrice, WeeklyBasketItem
from accounts.models import User
from tasks.models import PublishTask


class MemberOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("created at")
    )
    reference_task = models.ForeignKey(
        PublishTask, related_name='associated_reference_task',
        on_delete=models.CASCADE, verbose_name=_("reference task")
    )
    total_cost = models.FloatField(default=0.0, verbose_name=_("total cost"))

    class Meta:
        verbose_name = _("member order")

    def __str__(self):
        return (
            f"{self.user.username} added "
            f"on {self.created_at.strftime('%Y-%m-%d')}"
        )

    def update_total_cost(self):
        self.total_cost = sum(item.price for item in self.baskets.all())
        self.save()

    def is_active(self):
        return self.reference_task.published_at >= get_beginning_of_week()


class MemberSelectedBasket(models.Model):
    """
    MemberSelectedBasket keeps track of which and how many of a particular
    weekly basket of goods is chosen by the user (as a part of their weekly
    MemberOrder)

    Fetch the price of the basket and multiply by units desired. This number is
    added to the running total of the weekly order in MemberOrder.
    """
    order = models.ForeignKey(
        MemberOrder, on_delete=models.CASCADE, related_name='baskets',
        verbose_name=_("order")
    )
    basket = models.ForeignKey(
        Basket, on_delete=models.CASCADE, verbose_name=_("basket")
    )
    quantity = models.PositiveIntegerField(
        default=0, verbose_name=_("quantity")
    )
    price = models.FloatField(blank=True, null=True, verbose_name=_("price"))

    class Meta:
        verbose_name = _("member selected basket")

    def save(self, *args, **kwargs):
        # Calculate the total price based on the latest price of the basket
        latest_price = BasketPrice.objects\
            .filter(basket=self.basket).order_by('-date').first()
        self.price = latest_price.price * self.quantity
        super().save(*args, **kwargs)
        self.order.update_total_cost()

    def delete(self, *args, **kwargs):
        order = self.order
        super().delete(*args, **kwargs)
        order.update_total_cost()

    def __str__(self):
        return f"{self.quantity} of {self.basket.name}"


class DistributorOrder(models.Model):
    member_orders = models.ManyToManyField(
        'MemberOrder', related_name='distributor_orders',
        verbose_name=_("member orders")
    )
    order_for_week_of = models.DateField(
        blank=True, null=True, verbose_name=_("order for week of")
    )
    valid_until = models.DateField(
        blank=True, null=True, verbose_name=_("valid until")
    )
    total_orders = models.PositiveIntegerField(
        default=0, verbose_name=_("total orders")
    )
    total_budget = models.FloatField(
        default=0.00, verbose_name=_("Total budget")
    )
    total_purchase_cost = models.FloatField(
        default=0.00, verbose_name=_("total purchase cost")
    )

    class Meta:
        verbose_name = _("distributor order")

    def save(self, *args, **kwargs):
        # Calculate the start of the week (Monday)
        if self.order_for_week_of is None:  # Only set if order_for_week_of is not already set
            start_of_week = date.today() - timedelta(days=date.today().weekday())
            self.order_for_week_of = start_of_week
        # Save the instance first to get an ID
        super().save(*args, **kwargs)

        # Retrieve all MemberOrder instances and filter for active ones
        active_member_orders = [order for order in MemberOrder.objects.all() if order.is_active()]

        # Set the member orders for this distributor order
        self.member_orders.set(active_member_orders)

    def update_totals(self):
        self.total_budget = sum(
            basket.price for order in self.member_orders.all() for basket in order.baskets.all()
        )
        self.total_orders = self.member_orders.count()
        self.total_purchase_cost = sum(
            basket.basket_cost for basket in self.basket_orders.all()
        )

    def is_active(self):
        return self.valid_until >= date.today()

    def __str__(self):
        return f"Distributor Order for week of {self.order_for_week_of}"


class DistributorOrderBasket(models.Model):
    distributor_order = models.ForeignKey(
        DistributorOrder, related_name='basket_orders',
        on_delete=models.CASCADE, verbose_name=_("distributor order")
    )
    basket_name = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("basket name")
    )
    basket_quantity = models.PositiveIntegerField(
        default=0, verbose_name=_("basket quantity")
    )
    total_basket_budget = models.FloatField(
        default=0.00, verbose_name=_("Total basket budget")
    )
    basket_cost = models.FloatField(
        default=0.00, verbose_name=_("basket cost"))

    class Meta:
        verbose_name = _("distributor order basket")

    def __str__(self):
        return f"{self.basket_name}"

    def transform_distributor_order_to_member_baskets(self):
        """
        Proposes an initial set of item quantities to purchase at the
        distributor to make the most use of the total budget. The optimization
        logic is such that we're looking to purchase roughly the same number of
        "units" per item in a basket. Once we have an order model, compute the
        relevant fields in `DistributorOrderBasketItem`
        """
        basket_items = self.basket_order_items.all()
        item_prices = {item.id: item.weekly_basket_item.product.latest_price for item in basket_items}
        # Create the optimization model
        model = LpProblem("Optimal basket item purchase", LpMaximize)
        # Create a variable for each item, representing the count of that item
        item_vars = {item_id: LpVariable(f"item_{item_id}", lowBound=0, cat='Integer') for item_id in item_prices.keys()}
        min_count = LpVariable("min_count", lowBound=0, cat='Integer')
        # Add a variable for the difference from the budget
        difference_from_budget = LpVariable("Difference from budget", lowBound=0)
        # objective 1: maximize the total number of items
        model += lpSum(item_vars[item_id] for item_id in item_vars), "Total_Items"
        # Constraint 1: total price must not exceed the budget
        total_cost = lpSum(item_prices[item_id] * item_vars[item_id] for item_id in item_vars)
        model += total_cost <= self.total_basket_budget, "Basket budget"
        for item_id in item_vars:
            # constrain 2: ensure item count doesn't go below min_count
            model += item_vars[item_id] >= min_count, f"Min_count_constraint_{item_id}"
            # constrain 3: ensure no item is >=1 than min_count
            model += item_vars[item_id] <= min_count + 1, f"Max_difference_constraint_{item_id}"
        # constrain 4: minimize difference between basket budget and total cost
        model += difference_from_budget == self.total_basket_budget - total_cost, "Budget difference"
        # objective 2: minimize the difference from the budget
        model += -difference_from_budget, "Minimize budget difference"
        # Solve the model
        model.solve()
        for item in basket_items:
            # Update the DistributorOrderBasketItem directly
            item.quantity = int(item_vars[item.id].varValue)
            item.quantity_price = round(item.quantity * item.weekly_basket_item.product.latest_price, 2)
            item.units_per_basket = round(item.weekly_basket_item.product.units_by_packaging * item.quantity / self.basket_quantity, 1)
            item.cost_per_basket = round(item.quantity_price / self.basket_quantity, 2)
            item.save()
        # set basket_cost based on item optimization
        self.basket_cost = total_cost.value()
        self.save()


class DistributorOrderBasketItem(models.Model):
    distributor_order_basket = models.ForeignKey(
        DistributorOrderBasket, related_name='basket_order_items',
        on_delete=models.CASCADE,
        verbose_name=_("distributor order basket item")
    )
    weekly_basket_item = models.ForeignKey(
        WeeklyBasketItem, related_name='distributor_order_items',
        on_delete=models.CASCADE, verbose_name=_("weekly basket item")
    )
    quantity = models.PositiveIntegerField(
        default=0, verbose_name=_("quantity")
    )
    quantity_price = models.FloatField(
        default=0.00, verbose_name=_("quantity price")
    )
    units_per_basket = models.FloatField(
        default=0.0, verbose_name=_("units per basket")
    )
    cost_per_basket = models.FloatField(
        default=0.00, verbose_name=_("cost per basket")
    )

    class Meta:
        verbose_name = _("distributor order basket item")

    def __str__(self):
        return f"{self.weekly_basket_item}"


# Signal to update totals when member_orders are added or removed
@receiver(m2m_changed, sender=DistributorOrder.member_orders.through)
def update_distributor_order(sender, instance, action, **kwargs):
    """
    Whenever a DistributorOrder is started, compute global statistics on the
    order, and automatically build the DistributorOrderBaskets and their
    corresponding DistributorOrderBasketItems from the MemberOrders
    """
    if action == "post_add":
        # build DistributorOrderBaskets and their DistributorOrderBasketItems
        basket_summary = {}
        # Iterate through each MemberOrder in the DistributorOrder
        for member_order in instance.member_orders.all():
            # Iterate through each selected basket in the member order
            for selected_basket in member_order.baskets.all():
                basket_name = selected_basket.basket.name
                quantity = selected_basket.quantity
                price = selected_basket.price

                # If the basket name is not in the summary, initialize it
                if basket_name not in basket_summary:
                    basket_summary[basket_name] = {
                        'total_quantity': 0,
                        'total_price': 0.0
                    }

                # Update the total quantity and total price
                basket_summary[basket_name]['total_quantity'] += quantity
                basket_summary[basket_name]['total_price'] += price

        for basket_name, summary in basket_summary.items():
            distributor_order_basket = DistributorOrderBasket.objects.create(
                distributor_order=instance,
                basket_name=basket_name,
                basket_quantity=summary['total_quantity'],
                total_basket_budget=summary['total_price']
            )

            # Retrieve WeeklyBasketItems for the created DistributorOrderBasket
            weekly_basket_items = WeeklyBasketItem.objects.filter(basket__name=basket_name)
            # Create DistributorOrderBasketItems for each WeeklyBasketItem
            for weekly_basket_item in weekly_basket_items:
                DistributorOrderBasketItem.objects.create(
                    distributor_order_basket=distributor_order_basket,
                    weekly_basket_item=weekly_basket_item,
                    quantity=summary['total_quantity'],
                    quantity_price=0.00
                )
            # run transformation logic on distributor order items to member
            # orders
            distributor_order_basket.transform_distributor_order_to_member_baskets()

    # update distributor order global stats once the components are computed
    if action in ["post_add", "post_remove", "post_clear"]:
        instance.update_totals()
        instance.save(update_fields=['total_orders', 'total_budget', 'total_purchase_cost'])
