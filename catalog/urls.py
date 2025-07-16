from django.urls import path
from core.views import homepage_view
from users.views import ProfileView
from . import views
from .views import (
    product_detail_view,
    approve_payment,
    reject_payment,
    cart_view,
    add_to_cart_view,
    cart_increase_view,
    cart_decrease_view,
    cart_remove_view,
    checkout_view,
)

app_name = 'catalog'

urlpatterns = [
    path('', views.homepage_view, name='homepage'),
    path('products/', views.product_list_view, name='product_list'),
    path('search/', views.search_results, name='search_results'),
    path('contact/', views.contact_page_view, name='contact_page'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('orders/', views.order_list_view, name='order_list'),
    path('product/<int:id>/', product_detail_view, name='product_detail'),
    path('category/<slug:slug>/', views.category_products_view, name='category_products'),
    path('submit-payment/', views.submit_payment_view, name='submit_payment'),
    path('confirm-payment/<int:pk>/', approve_payment, name='approve_payment'),
    path('reject-payment/<int:pk>/', reject_payment, name='reject_payment'),
    
    # 🛒 مسیرهای سبد خرید
    path('cart/', cart_view, name='cart_view'),
    path('add-to-cart/<int:product_id>/', add_to_cart_view, name='add_to_cart'),
    path('cart/increase/<int:product_id>/', cart_increase_view, name='cart_increase'),
    path('cart/decrease/<int:product_id>/', cart_decrease_view, name='cart_decrease'),
    path('cart/remove/<int:product_id>/', cart_remove_view, name='cart_remove'),
    
    # 💳 مسیر پرداخت
    path('checkout/', checkout_view, name='checkout'),
]
