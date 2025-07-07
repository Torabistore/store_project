from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Order, OrderItem

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['mobile_number', 'first_name', 'last_name', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('mobile_number', 'password')}),
        ('اطلاعات شخصی', {'fields': ('first_name', 'last_name')}),
        ('مجوزها', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('تاریخ‌های مهم', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile_number', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    search_fields = ['mobile_number', 'first_name', 'last_name']
    ordering = ['mobile_number']
    filter_horizontal = ('groups', 'user_permissions',)

@admin.register(User)
class UserAdmin(CustomUserAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # تغییر 'is_completed' به 'status' در list_display
    list_display = ['id', 'user', 'order_date', 'status', 'total_price']
    # تغییر 'is_completed' به 'status' در list_filter
    list_filter = ['status', 'order_date']
    search_fields = ['user__mobile_number']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    list_filter = ['order__order_date']
    search_fields = ['product__name']