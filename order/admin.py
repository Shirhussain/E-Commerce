from django.contrib import admin
from .models import ShopCard


class ShopCardAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'quantity', 'price', 'amount']
    list_filter  = ['user']


admin.site.register(ShopCard, ShopCardAdmin)
