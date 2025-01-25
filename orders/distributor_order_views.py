import json
from django.http import JsonResponse
from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.views import View
from tasks.mixins import PermissionRequiredMixin
from orders.models import MemberOrder, DistributorOrder, DistributorOrderBasketItem
from baskets.utils import get_beginning_of_week
from datetime import date


class DistributorOrderView(PermissionRequiredMixin, View):
    template_name = 'distributor_order.html'
    group_name = 'Compile Member orders to generate a Distributor Order list'

    now = date.today()

    def get(self, request, *args, **kwargs):
        member_orders = MemberOrder.objects.prefetch_related('baskets')\
            .filter(reference_task__published_at__gte=get_beginning_of_week()).all()
        distributor_order = DistributorOrder.objects.prefetch_related(
            Prefetch(
                'basket_orders__basket_order_items',
                queryset=DistributorOrderBasketItem.objects.filter(
                    weekly_basket_item__valid_until__gte=self.now
                )
            )
        ).order_by('-order_for_week_of').first()

        # Calculate total cost for each basket_order
        if distributor_order:
            for basket_order in distributor_order.basket_orders.all():
                total_cost = sum(item.cost_per_basket for item in basket_order.basket_order_items.all())
                basket_order.total_cost = total_cost

        # Create a set of unique basket names
        member_baskets = sorted({basket.basket for order in member_orders for basket in order.baskets.all()}, key=lambda b: b.name)

        # Initialize the summary dictionary
        member_orders_summary = {
            'total_cost': 0,
            'baskets': {basket: 0 for basket in member_baskets}  # Initialize with sorted baskets
        }
        # Iterate through each order to populate the summary
        for order in member_orders:
            order.basket_quantities = {selected_basket.basket: selected_basket.quantity for selected_basket in order.baskets.all()}
            member_orders_summary['total_cost'] += order.total_cost

            # Update the basket summary
            for basket, quantity in order.basket_quantities.items():
                # Add the quantity to the corresponding basket in the summary
                member_orders_summary['baskets'][basket] += quantity

        context = {
            'task': self.group_name,
            'member_baskets': member_baskets,
            'member_orders': member_orders,
            'member_orders_summary': member_orders_summary,
            'distributor_order': distributor_order,
        }

        return render(request, self.template_name, context)


class CreateDistributorOrderView(PermissionRequiredMixin, View):
    template_name = 'distributor_order.html'
    group_name = 'Compile Member orders to generate a Distributor Order list'

    def post(self, request, *args, **kwargs):
        try:
            # Create a new DistributorOrder instance
            distributor_order = DistributorOrder.objects.create()

            # Redirect to the same view or another view after creation
            return redirect('distributor_order')  # Replace with the actual URL name for your view

        except Exception as e:
            # Redirect to a custom error page
            return render(request, '500.html', status=500)


class ModifyDistributorOrderBasketView(PermissionRequiredMixin, View):
    template_name = 'distributor_order.html'
    group_name = 'Compile Member orders to generate a Distributor Order list'

    def post(self, request, *args, **kwargs):
        # Check if the request is an AJAX request
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = data.get('quantity')

        # fetch the right basket item
        basket_item = DistributorOrderBasketItem.objects.get(
            weekly_basket_item__product__id=item_id
        )

        # Update the quantity and related fields
        basket_item.quantity = quantity
        basket_item.quantity_price = round(basket_item.quantity * basket_item.weekly_basket_item.product.latest_price, 2)
        basket_item.units_per_basket = round(basket_item.weekly_basket_item.product.units_by_packaging * basket_item.quantity / basket_item.distributor_order_basket.basket_quantity, 1)
        basket_item.cost_per_basket = round(basket_item.quantity_price / basket_item.distributor_order_basket.basket_quantity, 2)
        basket_item.save()

        # Update the associated DistributorOrderBasket
        distributor_order_basket = basket_item.distributor_order_basket
        distributor_order_basket.basket_cost = sum(item.quantity_price for item in distributor_order_basket.basket_order_items.all())
        distributor_order_basket.cost_per_basket = distributor_order_basket.basket_cost / distributor_order_basket.basket_quantity
        distributor_order_basket.save()

        # Update the associated DistributorOrder
        distributor_order = distributor_order_basket.distributor_order
        distributor_order.total_purchase_cost = sum(basket.basket_cost for basket in distributor_order.basket_orders.all())
        distributor_order.save()

        # Return a JSON response
        # Return a JSON response with updated values
        return JsonResponse({
            'status': 'success',
            'item_id': item_id,
            'basket_id': basket_item.distributor_order_basket.id,
            'quantity': quantity,
            'quantity_price': basket_item.quantity_price,
            'units_per_basket': basket_item.units_per_basket,
            'cost_per_item_per_basket': basket_item.cost_per_basket,
            'cost_per_basket': distributor_order_basket.cost_per_basket,
            'total_purchase_cost': distributor_order.total_purchase_cost,
            'basket_cost': distributor_order_basket.basket_cost,
            'total_budget': distributor_order_basket.total_basket_budget,
        })
