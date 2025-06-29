# catalog/urls.py

from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path('about/', views.about_page, name='about_page'), # <--- این خط اضافه شد
    path('contact/', views.contact_page, name='contact_page'), # <--- این خط اضافه شد
]