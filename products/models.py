from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=120)
    provider_code = models.CharField(max_length=120)
    provider = models.CharField(max_length=120)
    provider_price = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
    retailer_price = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
    wholesaler_price = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name
