from django.contrib import admin
from .models import MemberOrder, MemberSelectedBasket, DistributorOrder, DistributorOrderBasket, DistributorOrderBasketItem


class MemberSelectedBasketInline(admin.TabularInline):
    model = MemberSelectedBasket
    extra = 1


class DistributorOrderBasketInline(admin.TabularInline):
    model = DistributorOrderBasket
    extra = 1


@admin.register(MemberOrder)
class MemberOrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'total_cost', 'reference_task')
    search_fields = ('user__username',)
    inlines = [MemberSelectedBasketInline]


@admin.register(MemberSelectedBasket)
class MemberSelectedBasketAdmin(admin.ModelAdmin):
    list_display = ('order', 'basket', 'quantity', 'price')
    list_filter = ('order', 'basket')
    search_fields = ('order__user__username', 'basket__name')


@admin.register(DistributorOrder)
class DistributorOrderAdmin(admin.ModelAdmin):
    list_display = ('order_for_week_of', 'total_budget', 'total_orders', 'total_purchase_cost')
    search_fields = ('member_orders__user__username',)
    filter_horizontal = ('member_orders',)
    inlines = [DistributorOrderBasketInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('member_orders')

    def member_orders_count(self, obj):
        return obj.member_orders.count()
    member_orders_count.short_description = 'Number of Member Orders'


@admin.register(DistributorOrderBasketItem)
class DistributorOrderBasketItemAdmin(admin.ModelAdmin):
    list_display = ('weekly_basket_item', 'distributor_order_basket', 'quantity', 'quantity_price', 'units_per_basket', 'cost_per_basket')
    list_filter = ('distributor_order_basket', 'weekly_basket_item')
    search_fields = ('distributor_order_basket__distributor_order__order_for_week_of', 'weekly_basket_item__name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('distributor_order_basket', 'weekly_basket_item')
