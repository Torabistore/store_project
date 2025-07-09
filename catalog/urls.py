from django.urls import path
from . import views

app_name = 'catalog'


urlpatterns = [
    path('', views.homepage, name='homepage'),


    # 📦 لیست محصولات و دسته‌ها
    path('products/', views.product_list, name='product_list'),
    path('products/category/<slug:category_slug>/', views.product_list, name='category_products'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),

    # 🛒 مدیریت سبد خرید
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/remove/<int:item_id>/', views.cart_remove, name='cart_remove'),
    path('cart/increase/<int:item_id>/', views.cart_increase, name='cart_increase'),
    path('cart/decrease/<int:item_id>/', views.cart_decrease, name='cart_decrease'),

    # 🛍️ افزودن به سبد خرید (با انتخاب ویژگی‌ها)
    path('product/<int:product_id>/add-to-cart/', views.add_to_cart, name='add_to_cart'),

    # 🔍 جستجوی محصولات
    path('search/', views.search_results, name='search_results'),

    # 📄 صفحات ایستا
    path('about/', views.about_page, name='about_page'),
    path('contact/', views.contact_page, name='contact_page'),

    # 💳 صفحه پرداخت
    path('checkout/', views.checkout_view, name='checkout'),

]
