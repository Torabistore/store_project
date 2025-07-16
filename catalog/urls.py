from django.urls import path
from core.views import homepage_view
from . import views
from users.views import ProfileView 
from .views import approve_payment, product_detail_view, reject_payment
from django.urls import path
from .views import (
    cart_view,
    add_to_cart_view,
    cart_increase_view,
    cart_decrease_view,
    cart_remove_view,
)
from .views import checkout_view



app_name = 'catalog'

urlpatterns = [
    path('products/', views.product_list_view, name='product_list'),
    path('search/', views.search_results, name='search_results'),
    path('', homepage_view, name='catalog:homepage'),
    path('contact/', views.contact_page_view, name='contact_page'),
    path('profile/', ProfileView.as_view(), name='profile'),  # 👈 باید قبل از slug باشه
    path('orders/', views.order_list_view, name='order_list'),
    path('product/<int:id>/', product_detail_view, name='product_detail'),
    path('category/<slug:slug>/', views.category_products_view, name='category_products'),
    path('submit-payment/', views.submit_payment_view, name='submit_payment'),
    path('confirm-payment/<int:pk>/', approve_payment, name='approve_payment'),
    path('reject-payment/<int:pk>/', reject_payment, name='reject_payment'),
    path('cart/', cart_view, name='cart_view'),
    path('add-to-cart/<int:product_id>/', add_to_cart_view, name='add_to_cart'),
    path('cart/increase/<int:product_id>/', cart_increase_view, name='cart_increase'),
    path('cart/decrease/<int:product_id>/', cart_decrease_view, name='cart_decrease'),
    path('cart/remove/<int:product_id>/', cart_remove_view, name='cart_remove'),
    path('checkout/', checkout_view, name='checkout'),
    

]

