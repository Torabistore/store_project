from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (
    ContactMessage, CustomerDebt, PaymentRequest,
    Product, Category, ProductImage, ProductVariant
)

# ✉️ پیام‌های تماس
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'created_at')
    search_fields = ('full_name', 'email', 'message')
    list_filter = ('created_at', 'email')
    ordering = ['-created_at']
    readonly_fields = ('full_name', 'email', 'phone_number', 'message', 'created_at')


# 🎯 دسته‌بندی محصولات
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


# 🖼 تصاویر محصول
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'is_main', 'image_tag')
    readonly_fields = ('image_tag',)


# 🎨 ویژگی‌های محصول
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


# 🧺 محصول
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'formatted_price', 'available', 'category', 'created_at')
    list_filter = ('available', 'category')
    search_fields = ('name', 'description')
    inlines = [ProductImageInline, ProductVariantInline]
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('اطلاعات محصول', {
            'fields': (
                'name', 'slug', 'category', 'price',
                'available', 'image_caption', 'description', 'specifications'
            )
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
    prepopulated_fields = {'slug': ('name',)}


# 💳 بدهی مشتری
@admin.register(CustomerDebt)
class CustomerDebtAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_debt', 'updated_at')
    search_fields = ('user__username', 'user__phone_number')
    list_filter = ('updated_at',)

@admin.register(PaymentRequest)
class PaymentRequestAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'amount', 'status', 'created_at',
        'reference_number', 'receipt_tag', 'approve_button', 'reject_button'
    )
    search_fields = ('user__username', 'reference_number')
    list_filter = ('status', 'created_at')
    readonly_fields = (
        'user', 'amount', 'status', 'reference_number',
        'created_at', 'payment_receipt', 'receipt_tag',
        'approve_button', 'reject_button'
    )
    actions = ['approve_request']

    def approve_request(self, request, queryset):
        for req in queryset:
            if req.status == 'pending':
                req.approve()
        self.message_user(request, "✅ درخواست‌ها تایید شدند و بدهی‌ها به‌روز شد.")
    approve_request.short_description = "تایید درخواست و کاهش بدهی"

    def receipt_tag(self, obj):
        if obj.payment_receipt:
            return mark_safe(f'<img src="{obj.payment_receipt.url}" width="100">')
        return "فیشی ثبت نشده"
    receipt_tag.short_description = "فیش پرداختی"

    def approve_button(self, obj):
        if obj.status == 'pending':
            return mark_safe(f'<a class="button" href="/confirm-payment/{obj.id}/">✅ تأیید</a>')
        return '-'
    approve_button.short_description = 'تأیید'

    def reject_button(self, obj):
        if obj.status == 'pending':
            return mark_safe(f'<a class="button" href="/reject-payment/{obj.id}/">❌ رد</a>')
        return '-'
    reject_button.short_description = 'رد'

    class Media:
        css = {
            'all': ('admin/css/custom-admin.css',)
        }




