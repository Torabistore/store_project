# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import User, Order, OrderItem # وارد کردن مدل User سفارشی

# فرم سفارشی برای ایجاد کاربر در ادمین
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('mobile_number', 'first_name', 'last_name') # فیلدهای مورد استفاده در فرم ایجاد کاربر
        # اگر فیلد email را دارید، آن را نیز اضافه کنید.

# فرم سفارشی برای تغییر کاربر در ادمین
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('mobile_number', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'last_login') # 'date_joined' حذف شد 

# کلاس Admin برای مدل User سفارشی
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('mobile_number', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('mobile_number', 'first_name', 'last_name')
    ordering = ('mobile_number',)

    fieldsets = (
        (None, {'fields': ('mobile_number', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                     'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}), # 'date_joined' در اینجا (fieldsets) برای نمایش است و معمولاً مشکل‌ساز نیست.
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile_number', 'first_name', 'last_name', 'password', 'password2'),
        }),
    )

# کلاس‌های admin برای Order و OrderItem
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_date', 'total_price', 'is_completed')
    list_filter = ('is_completed', 'order_date')
    search_fields = ('user__mobile_number', 'id')
    inlines = [OrderItemInline]
    readonly_fields = ('order_date', 'total_price')