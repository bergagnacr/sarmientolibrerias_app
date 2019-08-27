from django.urls import path, include
from .views import products_import_home, products_home

app_name = 'products'

urlpatterns = [
    path('', products_home, name='products_home'),
    path('import/', products_import_home, name='import_lists'),
]
