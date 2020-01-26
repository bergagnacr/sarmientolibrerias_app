from django.urls import path, include
from .views import products_import_home, products_home, products_home_json

app_name = 'products'

urlpatterns = [
    path('json/', products_home_json, name='json'),
    path('', products_home, name='products_home'),
    path('import/', products_import_home, name='import_lists'),
]
