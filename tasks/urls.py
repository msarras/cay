from django.urls import path

from .task_handling_views import (
    TaskView,
    CancelTaskAssignmentView,
    ModifyTaskAssignmentView,
    task_assigned,
)
from .weekly_basket_handling_views import (
    CreateWeeklyBasketsView,
    ManageWeeklyBasketItemsView,
    published_baskets
)

app_name = 'tasks'

urlpatterns = [
    path('list/', TaskView.as_view(), name='list'),
    path('task-assigned/', task_assigned, name='task_assigned'),
    path('cancel-task-assignment/', CancelTaskAssignmentView.as_view(), name='cancel_task_assignment'),
    path('modify-task-assignment/', ModifyTaskAssignmentView.as_view(), name='modify_task_assignment'),
    path('create-weekly-baskets/', CreateWeeklyBasketsView.as_view(), name='create_weekly_baskets'),
    path('manage-weekly-basket-items/<int:basket_id>/', ManageWeeklyBasketItemsView.as_view(), name='manage_weekly_basket_items'),
    path('published-weekly-baskets/', published_baskets, name='published_weekly_baskets'),
]
