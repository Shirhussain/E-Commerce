from django.urls import path

from . import views

app_name = "user"
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_form, name='login'),
    path('signup/', views.signup_form, name='signup'),
    path('logout/', views.logout_form, name='logout'),
]