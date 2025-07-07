from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('set-new-password/<uidb64>/<token>/', views.set_new_password, name='set_new_password'),

    path('profile/', views.profile_view, name='profile'),
    path('orders/', views.order_list_view, name='order_list'),
]
