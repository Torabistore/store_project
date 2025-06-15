# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views # ویوهای پیش‌فرض جنگو برای احراز هویت
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='homepage'), name='logout'), # بعد از خروج به صفحه اصلی برمی‌گردد
    path('profile/', views.profile, name='profile'),
    path('orders/', views.order_list, name='order_list'), # برای مشاهده لیست سفارشات
]