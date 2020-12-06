from django.urls import path

from . import views

app_name = "order"
urlpatterns = [
    path('', views.index, name='index'),
    path('shop-card', views.shop_card, name='shop-card'),
    path('delete-from-card/<int:id>/', views.delete_from_card, name='delete-from-card'),
    path('add-to-shop-card/<int:id>/', views.add_to_card, name='add-to-card'),
]