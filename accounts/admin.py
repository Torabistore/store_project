# accounts/admin.py
from django.contrib import admin
from django.utils.html import mark_safe # این را برای نمایش پیش‌نمایش عکس وارد می‌کنیم
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0 # به صورت پیش‌فرض، هیچ فیلد خالی اضافی برای آیتم سفارش جدید نشان نمی‌دهد
    readonly_fields = ('product', 'quantity', 'price') # این فیلدها فقط برای نمایش هستند و قابل ویرایش نیستند

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_date', 'total_price', 'is_completed')
    list_filter = ('is_completed', 'order_date')
    search_fields = ('user__username', 'id')
    inlines = [OrderItemInline] # نمایش آیتم‌های سفارش در صفحه جزئیات سفارش
    readonly_fields = ('order_date', 'total_price') # این فیلدها نباید دستی تغییر کنند