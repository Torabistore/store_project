from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.homepage_view, name='homepage'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', views.password_reset_request, name='reset_password'),
    path('password-reset/verify/', views.verify_otp, name='verify_otp'),
    path('password-reset/new/', views.set_new_password, name='set_new_password'),
    path('profile/', views.profile_view, name='profile'),
    path('order-list/', views.order_list_view, name='order_list'),
    

]
