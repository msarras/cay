# products/urls.py
from django.urls import path
from .views import (
    UploadProductsView
)

urlpatterns = [
    path('upload-product-prices/', UploadProductsView.as_view(), name='upload_products'),
]
