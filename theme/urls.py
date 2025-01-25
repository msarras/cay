from django.urls import path
from .views import switch_language

urlpatterns = [
    path('switch_language/<str:lang_code>/', switch_language, name='switch_language'),
]
