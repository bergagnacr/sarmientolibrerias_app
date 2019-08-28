from django.contrib import admin
from products.models import Product

# Register your models here.


class ProductsAdmin(admin.ModelAdmin):
    list_display = ['__provider_code__', '__str__', '__provider__', '__provider_price__', '__updated__']

    class Meta:
        model = Product


admin.site.register(Product, ProductsAdmin)
