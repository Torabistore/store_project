# D:\store_project\catalog\urls.py

from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('about/', views.about_page, name='about_page'),
    path('contact/', views.contact_page, name='contact_page'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]