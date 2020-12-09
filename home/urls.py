from django.urls import path

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about_us, name='about-us'),
    path('contact/', views.contact_us, name='contact-us'),
    path('search/', views.search, name='search'),
    path('search_auto/', views.search_auto, name='search-auto'),
    path('comment/<int:id>/', views.add_comment, name='add-comment'),
    path('category/<int:id>/<slug:slug>/', views.category_product, name='category-product'),
    path('product-detail/<int:id>/<slug:slug>/', views.product_detail, name='product-detail'),
    path('faq/', views.faq, name='faq'),
]