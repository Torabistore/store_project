# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'), # <--- این خط اضافه شد
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('set-new-password/', views.set_new_password, name='set_new_password'),
    path('orders/', views.order_list, name='order_list'),
]