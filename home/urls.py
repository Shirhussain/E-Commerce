from django.urls import path

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about_us, name='about-us'),
    path('contact/', views.contact_us, name='contact-us'),
    path('category/<int:id>/<slug:slug>/', views.category_product, name='category-product'),
]