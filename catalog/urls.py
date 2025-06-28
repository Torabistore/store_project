# catalog/urls.py
from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    # این خط قبلاً homepage بود، بهتر است به نام واقعی‌اش یعنی product_list باشد
    path('', views.product_list, name='product_list'), 

    # URL های جدید برای صفحات درباره ما و تماس با ما
    path('about/', views.about_page, name='about_page'),
    path('contact/', views.contact_page, name='contact_page'),

    # سایر URL های مربوط به کاتالوگ شما در اینجا قرار می‌گیرند...
    # path('product/<int:pk>/', views.product_detail, name='product_detail'),
]