from django.contrib import admin
from .models import Category, Product, ProductImage, ProductVariant
from django.utils.html import format_html

# 📸 نمایش تصاویر محصول به‌صورت اینلاین
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


# 🎨 نمایش ویژگی‌های محصول به‌صورت اینلاین (اختیاری)
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0
    fields = ('color', 'size', 'stock', 'price')
    readonly_fields = []

# 🗂️ مدیریت دسته‌بندی‌ها
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


# 🛍️ مدیریت محصولات
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'formatted_price', 'available', 'created_at', 'updated_at', 'category', 'main_image_tag']
    list_filter = ['available', 'created_at', 'updated_at', 'category']
    list_editable = ['available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description', 'specifications']
    inlines = [ProductImageInline, ProductVariantInline]
    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'slug', 'description', 'specifications', 'price', 'available')
        }),
    )

    def formatted_price(self, obj):
        return f"{obj.price:,.0f} تومان"
    formatted_price.short_description = 'قیمت'

    def main_image_tag(self, obj):
        main_image = obj.images.filter(is_main=True).first() or obj.images.first()
        if main_image:
            return format_html('<img src="{}" style="width: 100px; height: 100px;" />', main_image.image.url)
        return "-"
    main_image_tag.short_description = 'تصویر اصلی'


# 📷 مدیریت مستقیم تصاویر محصول
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'is_main']
    list_filter = ['product']


# 👕 مدیریت ویژگی‌های انتخابی محصول
@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'color', 'size', 'stock', 'price']
    list_filter = ['product', 'color', 'size']
    search_fields = ['color', 'size']
