from django import template
from django.db.models import Sum
from django.urls import reverse

from mysite import settings
from order.models import ShopCard
from product.models import Category

register = template.Library()


@register.simple_tag
def categorylist():
    return Category.objects.all()

@register.simple_tag
def shopcardcount(userid):
    count = ShopCard.objects.filter(user_id=userid).count()
    return count


