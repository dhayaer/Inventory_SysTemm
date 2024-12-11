from django.urls import path
from .views import create_product, list_products, add_stock, remove_stock
from . import views
from django.http import JsonResponse
from products.views import remove_product  # This will cause an error if remove_product is not defined

urlpatterns = [
    path('', lambda request: JsonResponse({'message': 'Welcome to the API'}, status=200)),
    path('create-product/', views.create_product, name='create-product'),
    path('list-products/', list_products, name='list-products'),
    path('add-stock/', views.add_stock, name='add-stock'),
    path('remove-stock/', views.remove_stock, name='remove-stock'),
    path('api/remove-product/', remove_product, name='remove-product'),
]