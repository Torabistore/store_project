from django.contrib import admin
from .models import Category, Product, ProductImage, ProductVariant
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('created_at', 'email')  # 🆕 فیلتر بر اساس تاریخ و ایمیل
    ordering = ['-created_at']  # 🆕 مرتب‌سازی پیش‌فرض با جدیدترین بالا
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'is_main', 'image_tag')
    readonly_fields = ('image_tag',)


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'formatted_price', 'available', 'category', 'created_at')
    list_filter = ('available', 'category')
    search_fields = ('name', 'description')
    inlines = [ProductImageInline, ProductVariantInline]

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

    readonly_fields = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
