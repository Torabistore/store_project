from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('about/', views.about_page, name='about_page'),
    path('contact/', views.contact_page, name='contact_page'),
    
    # سبد خرید
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]
