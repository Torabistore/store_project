# catalog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # مسیر جدید: صفحه اصلی سایت حالا به این ویو اشاره می‌کند
    path('', views.homepage, name='homepage'),

    # مسیر جدید: لیست کامل محصولات به این آدرس منتقل شده
    path('products/', views.product_list, name='product_list'),

    path('category/<str:category_name>/', views.product_list, name='category_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('search/', views.search_results, name='search_results'),
    path('about/', views.about_page, name='about_page'),
    path('contact/', views.contact_page, name='contact_page'),
]