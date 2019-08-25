from django.db import models
from django.db.models import Q

# Create your models here.


class ProductManager(models.Manager):
    def all(self):
        return self.get_queryset()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().search(query)


class Product(models.Model):
    # name = models.CharField(max_length=120)
    title = models.CharField(max_length=120)
    provider_code = models.CharField(max_length=120)
    provider = models.CharField(max_length=120)
    provider_price = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    # retailer_price = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
    # wholesaler_price = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    # timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def __provider_code__(self):
        return self.provider_code

    def __provider__(self):
        return self.provider

    def __provider_price__(self):
        return self.provider_price

    def __updated__(self):
        return self.updated



