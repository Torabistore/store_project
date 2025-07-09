from django.contrib import admin
from .models import Category, Product, ProductImage, ProductVariant


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
    list_display = ('name', 'formatted_price', 'available', 'piece_count', 'category', 'created_at')
    list_filter = ('available', 'category')
    search_fields = ('name', 'description')
    inlines = [ProductImageInline, ProductVariantInline]

    fieldsets = (
        ('اطلاعات محصول', {
            'fields': (
                'name', 'slug', 'category', 'price', 'piece_count',
                'available', 'image_caption', 'description', 'specifications'
            )
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    readonly_fields = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
