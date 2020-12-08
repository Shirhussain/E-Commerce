from django.contrib import admin
from .models import ShopCard, Order, OrderProduct



class ShopCardAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'quantity', 'price', 'amount']
    list_filter  = ['user']


class OrderProductLine(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user', 'product', 'quantity', 'price', 'amount')
    can_delete = False 
    # when dealing with inlines in the admin one could set extra=0 to prevent a user to add a new related model.
    extra = 0 


class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'city','total','status']
    list_filter = ['status']
    readonly_fields = ('user','first_name','last_name','phone','address','city','country','total','ip')
    can_delete = False
    inlines = [OrderProductLine]


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'price', 'quantity', 'amount', 'status', 'updated_at']
    list_filter = ['user','status']


admin.site.register(ShopCard, ShopCardAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
