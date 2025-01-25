from django.urls import path, include

from .views import ProfileView

app_name = 'accounts'

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
]
