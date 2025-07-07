from django.contrib import admin
from .models import Category, Product, ProductImage
from django.utils.html import format_html

# Inline برای تصاویر محصول
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ['image_tag']
    fields = ('image', 'is_main', 'image_tag')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: 100px;" />', obj.image.url)
        return "-"
    
    image_tag.short_description = 'پیش‌نمایش'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'available', 'created_at', 'updated_at', 'category', 'main_image_tag']
    list_filter = ['available', 'created_at', 'updated_at', 'category']
    list_editable = ['available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description', 'specifications']
    inlines = [ProductImageInline]
    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'slug', 'description', 'specifications', 'price', 'available')
        }),
    )

    def main_image_tag(self, obj):
        main_image = obj.images.filter(is_main=True).first() or obj.images.first()
        if main_image:
            return format_html('<img src="{}" style="width: 100px; height: 100px;" />', main_image.image.url)
        return "-"
    
    main_image_tag.short_description = 'تصویر اصلی'

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'is_main']
    list_filter = ['product']
