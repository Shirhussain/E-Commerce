from django.urls import path

from . import views

app_name = "user"
urlpatterns = [
    path('', views.index, name='profile'),
    path('login/', views.login_form, name='login'),
    path('signup/', views.signup_form, name='signup'),
    path('logout/', views.logout_form, name='logout'),
    path('update/', views.user_update, name='user-update'),
    path('password/', views.user_password, name='password'),
    path('comment/', views.user_comment, name='user-comment'),
    path('comment/delete/<int:id>/', views.user_comment_delete, name='comment-delete'),
    path('order/', views.user_order, name='order'),
    path('order/detail/<int:id>/', views.user_order_detail, name='order-detail'),
    path('order/product/', views.user_order_product, name='order-product'),
    path('order/product-detail/<int:id>/<int:oid>/', views.user_order_product_detail, name='order-product-detail'),
]