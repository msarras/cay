from datetime import datetime, date, time
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Prefetch

from .mixins import PermissionRequiredMixin
from baskets.models import Basket, WeeklyBasketItem
from products.models import Product
from tasks.models import Task, PublishTask
from tasks.utils import get_end_of_week
from baskets.utils import get_beginning_of_week


class CreateWeeklyBasketsView(PermissionRequiredMixin, View):
    template_name = 'create_weekly_basket.html'
    group_name = 'Create and manage weekly basket'
    now = datetime.now()

    def get(self, request, *args, **kwargs):
        filtered_basket_items = WeeklyBasketItem.objects.filter(valid_until__gte=self.now)
        baskets = Basket.objects.prefetch_related(
            'prices',
            Prefetch('basket_items', queryset=filtered_basket_items)
        ).all()
        context = {
            'task': self.group_name,
            'baskets': baskets,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, name='manage_weekly_basket')
        date = request.POST.get('date')
        time = request.POST.get('time')

        # Convert strings to date and time objects
        date_obj = datetime.strptime(date, '%m/%d/%Y').date()
        time_obj = datetime.strptime(time, '%H:%M').time()
        # Combine date and time into a datetime object
        expiration_date = datetime.combine(date_obj, time_obj)

        # create the permissions object for accessing the basket with the
        # selected expiration date
        PublishTask.objects.create(task=task, valid_until=expiration_date)
        return redirect('tasks:published_weekly_baskets')


class ManageWeeklyBasketItemsView(PermissionRequiredMixin, View):
    template_name = 'manage_weekly_basket_items.html'
    group_name = 'Create and manage weekly basket'
    now = datetime.now()

    def get(self, request, *args, **kwargs):
        basket_id = kwargs.get('basket_id')
        basket = get_object_or_404(Basket, id=basket_id)
        basic_food_categories = basket.basic_foods.values_list('category', flat=True)
        basket_products = Product.objects.prefetch_related('basic_foods').filter(
            basic_foods__category__in=basic_food_categories).distinct()

        weekly_basket_items = WeeklyBasketItem.objects.filter(
            basket=basket,
            valid_until__gte=self.now
        ).distinct().values_list('product_id', flat=True)

        context = {
            'task': self.group_name,
            'basket': basket,
            'products': basket_products,
            'weekly_basket_items': weekly_basket_items,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        basket_id = kwargs.get('basket_id')
        basket = get_object_or_404(Basket, id=basket_id)
        product_id = request.POST.get('product_id')

        if product_id:
            product = get_object_or_404(Product, id=product_id)
            weekly_basket_item = WeeklyBasketItem.objects.filter(basket=basket, product=product).first()

            if weekly_basket_item:
                # If it exists, remove it
                weekly_basket_item.delete()
                action = 'removed'
            else:
                # If it doesn't exist, add it
                WeeklyBasketItem.objects.create(
                    basket=basket,
                    product=product,
                    week_of=get_beginning_of_week(),
                    valid_until=get_end_of_week(),
                )
                action = 'added'

            return JsonResponse({'status': 'success', 'action': action})

        return JsonResponse({'status': 'error'}, status=400)


@login_required
def published_baskets(request):
    return render(request, 'published_weekly_basket.html')
