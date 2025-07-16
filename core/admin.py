from django.contrib import admin
from .models import Product, ProductImage, Order, OrderItem
from .models import PaymentRequest

# ✅ محصول
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'available', 'created_at']
    list_filter = ['available', 'created_at']
    search_fields = ['name']
    inlines = [ProductImageInline]


# ✅ سفارش
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'total_price']
    list_filter = ['created_at']
    search_fields = ['user__username']
    inlines = [OrderItemInline]


# ✅ آیتم‌های سفارش (نمای جداگانه در صورت نیاز)
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    list_filter = ['order']
    search_fields = ['product__name']



@admin.register(PaymentRequest)
class PaymentRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'status', 'created_at', 'reference_number']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'reference_number']
    readonly_fields = ['payment_receipt']
