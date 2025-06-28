from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # مرحله اول: درخواست کد
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    
    # مرحله دوم: تایید کد
    path('verify-otp/', views.verify_otp, name='verify_otp'), 
    
    # مرحله سوم و نهایی: تنظیم رمز جدید
    path('set-new-password/', views.set_new_password, name='set_new_password'),
]
