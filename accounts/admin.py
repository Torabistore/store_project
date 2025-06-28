# accounts/admin.py

from django.contrib import admin
from .models import User, Order, OrderItem

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    تنظیمات نمایش مدل User در پنل ادمین
    """
    list_display = ('mobile_number', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('mobile_number', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')
    ordering = ('mobile_number',)


class OrderItemInline(admin.TabularInline):
    """
    تنظیمات نمایش آیتم‌های سفارش به صورت خطی در صفحه سفارش
    """
    model = OrderItem
    # فعلا فیلدی برای نمایش در این بخش نداریم چون محصول و قیمت را بعدا کامل می‌کنیم
    # readonly_fields را خالی می‌گذاریم تا خطایی رخ ندهد
    readonly_fields = ()
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    تنظیمات نمایش مدل Order در پنل ادمین
    """
    list_display = ('id', 'user', 'order_date', 'is_completed', 'total_price')
    list_filter = ('is_completed', 'order_date')
    search_fields = ('user__mobile_number', 'id')
    inlines = [OrderItemInline]
    
    # 'total_price' و 'order_date' چون به صورت خودکار محاسبه یا ثبت می‌شوند،
    # باید فقط خواندنی باشند.
    readonly_fields = ('order_date', 'total_price')