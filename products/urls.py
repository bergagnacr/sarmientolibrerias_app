from django.urls import path, include
from .views import products_import_home

app_name = 'products'

urlpatterns = [
    path('', products_import_home, name='import_lists'),
]
