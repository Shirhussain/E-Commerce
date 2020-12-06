from django.db import models
from django.contrib.auth.models import User

from product.models import Product


class ShopCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.title

    @property
    def price(self):
        return self.product.price 

    @property
    def amount(self):
        return (self.quantity*self.product.price)
        
