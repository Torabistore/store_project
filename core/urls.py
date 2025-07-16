from django.urls import path
from . import views
from users.views import CustomLoginView
from .views import register_view as signup_view
from core.views import login_view
from catalog.views import product_detail_view




app_name = 'core'

urlpatterns =[

    # 🔷 صفحات عمومی
    path('', views.homepage_view, name='homepage'),
    path('about/', views.about_page_view, name='about_page'),
    path('contact/', views.contact_page_view, name='contact_page'),
    path('product/<int:id>/', product_detail_view, name='product_detail'),

    # 🔐 احراز هویت
    path('login/', login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', signup_view, name='signup'), 
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile-image/', views.edit_profile_image, name='edit_profile_image'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),
    path('debts/', views.customer_debts_view, name='customer_debts'),
    path('addresses/', views.address_list_view, name='address_list'),
    
    # 📦 سفارشات
    path('orders/', views.order_list_view, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail_view, name='order_detail'),

    # 🔑 بازیابی رمز عبور
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('set-new-password/', views.set_new_password, name='set_new_password'),
    path('change-password/', views.password_change_view, name='password_change'),

]
