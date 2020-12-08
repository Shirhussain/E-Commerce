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
]