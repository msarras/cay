from django.urls import path
from .member_order_views import (
    BasketsView,
    ModifyOrderView,
    CancelOrderView,
    received_order
)
from .distributor_order_views import (
    CreateDistributorOrderView,
    DistributorOrderView,
    ModifyDistributorOrderBasketView
)


urlpatterns = [
    path('weekly_baskets/', BasketsView.as_view(), name='weekly_baskets'),
    path('submit_order/', BasketsView.as_view(), name='submit_order'),
    path('received_order/', received_order, name='received_order'),
    path('modify_order/', ModifyOrderView.as_view(), name='modify_order'),
    path('cancel_order/', CancelOrderView.as_view(), name='cancel_order'),
    path('distributor_order/', DistributorOrderView.as_view(), name='distributor_order'),
    path('create_distributor_order/', CreateDistributorOrderView.as_view(), name='create_distributor_order'),
    path('modify_distributor_order_basket/', ModifyDistributorOrderBasketView.as_view(), name='modify_distributor_order_basket'),
]
