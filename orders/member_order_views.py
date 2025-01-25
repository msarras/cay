from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView

from .models import MemberOrder, MemberSelectedBasket
from baskets.models import Basket, WeeklyBasketItem
from tasks.models import Task, PublishTask


class BaseBasketView(LoginRequiredMixin):
    today = date.today()

    def get_task(self):
        task_name = 'manage_weekly_basket'
        return get_object_or_404(Task, name=task_name)

    def get_active_publish_task(self, task):
        return PublishTask.objects.filter(
            task=task,
            published_at__lte=self.today,
            valid_until__gte=self.today
        ).first()

    def get_existing_order(self):
        task = self.get_task()
        return MemberOrder.objects.filter(
            user=self.request.user,
            reference_task=self.get_active_publish_task(task)
        ).first()

    def get_selected_baskets(self, order):
        return MemberSelectedBasket.objects.filter(order=order)


class BasketsView(BaseBasketView, TemplateView):
    template_name_existing_order = 'member_order_summary.html'
    template_name_weekly_baskets = 'weekly_baskets.html'
    template_name_weekly_basket_closed = 'weekly_basket_closed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_order = self.get_existing_order()

        if not self.get_active_publish_task(self.get_task()):
            self.template_name = self.template_name_weekly_basket_closed
            return context

        if existing_order:
            selected_baskets = self.get_selected_baskets(existing_order)
            total_price = sum(selected_basket.price for selected_basket in selected_baskets)
            context.update({
                'selected_baskets': selected_baskets,
                'total_price': total_price,
            })
            self.template_name = self.template_name_existing_order
        else:
            weekly_items = WeeklyBasketItem.objects.filter(valid_until__gte=self.today)
            baskets = Basket.objects.prefetch_related(
                Prefetch('basket_items', queryset=weekly_items)
            ).filter(basket_items__valid_until__gt=self.today).distinct()
            context['baskets'] = baskets
            self.template_name = self.template_name_weekly_baskets

        return context

    def post(self, request, *args, **kwargs):
        selected_baskets = {}
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                basket_name = key.split('_')[1]
                quantity = int(value)
                if quantity > 0:
                    selected_baskets[basket_name] = quantity

        if not selected_baskets:
            # If no items are selected, add an error message to the context
            context = self.get_context_data(**kwargs)
            context['error_message'] = "You must select at least one item to submit your order."
            return self.render_to_response(context)

        # Create a new MemberOrder based on selected baskets
        order = MemberOrder.objects.create(
            user=request.user,
            reference_task=self.get_active_publish_task(self.get_task())
        )

        for basket_name, quantity in selected_baskets.items():
            basket = get_object_or_404(Basket, name=basket_name)
            MemberSelectedBasket.objects.create(
                order=order,
                basket=basket,
                quantity=quantity,
                price=basket.prices.last().price
            )

        return redirect('received_order')  # Redirect to a success page or back to baskets


class ModifyOrderView(BaseBasketView, View):
    template_name = 'member_modify_order.html'

    def get(self, request):
        existing_order = self.get_existing_order()
        if existing_order:
            selected_baskets = self.get_selected_baskets(existing_order)
            # Create a dictionary to hold basket quantities
            basket_quantities = {selected_basket.basket.name: selected_basket.quantity for selected_basket in selected_baskets}
            # Fetch available baskets
            weekly_items = WeeklyBasketItem.objects.filter(valid_until__gte=self.today)
            baskets = Basket.objects.prefetch_related(
                Prefetch('basket_items', queryset=weekly_items)
            ).filter(basket_items__valid_until__gt=self.today).distinct()
            return render(request, self.template_name, {
                'selected_baskets': selected_baskets,
                'baskets': baskets,
                'basket_quantities': basket_quantities
            })
        return redirect('weekly_baskets')

    def post(self, request):
        existing_order = MemberOrder.objects.filter(
            user=request.user,
            created_at__gte=request.user.last_login.date()
        ).first()

        if existing_order:
            # Collect selected quantities from the form
            selected_baskets = {}
            for key, value in request.POST.items():
                if key.startswith('quantity_'):
                    basket_name = key.split('_')[1]  # Extract the basket name
                    quantity = int(value)  # Convert the quantity to an integer
                    if quantity >= 0:  # Allow zero to remove the basket
                        selected_baskets[basket_name] = quantity

            # Check if the total quantity is at least 1
            total_quantity = sum(selected_baskets.values())
            if total_quantity < 1:
                # Add an error message to the context
                error_message = "You must select at least one item."
                baskets = Basket.objects.filter(
                    basket_items__valid_until__gte=date.today()
                ).distinct()
                selected_baskets_db = MemberSelectedBasket.objects.filter(order=existing_order)

                # Create a dictionary to hold basket quantities
                basket_quantities = {selected_basket.basket.name: selected_basket.quantity for selected_basket in selected_baskets_db}

                return render(request, self.template_name, {
                    'selected_baskets': selected_baskets_db,
                    'baskets': baskets,
                    'basket_quantities': basket_quantities,
                    'error_message': error_message  # Pass the error message to the template
                })

            # Update existing MemberSelectedBasket entries
            for basket_name, quantity in selected_baskets.items():
                basket = get_object_or_404(Basket, name=basket_name)
                if quantity > 0:
                    # Update the existing entry
                    selected_basket, created = MemberSelectedBasket.objects.update_or_create(
                        order=existing_order,
                        basket=basket,
                        defaults={'quantity': quantity, 'price': basket.prices.last().price}
                    )
                else:
                    # If quantity is 0, delete the entry
                    MemberSelectedBasket.objects.filter(order=existing_order, basket=basket).delete()

            return redirect('received_order')

        return redirect('weekly_baskets')


class CancelOrderView(LoginRequiredMixin, View):
    def post(self, request):
        start_of_week = date.today() - timedelta(days=date.today().weekday())
        existing_order = MemberOrder.objects.filter(
            user=request.user,
            created_at__gte=request.user.last_login.date()
        )

        if existing_order:
            # Delete the existing order
            existing_order.delete()

        return redirect('weekly_baskets')  # Redirect to the weekly baskets view


@login_required
def received_order(request):
    return render(request, 'received_order.html')
