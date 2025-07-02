# catalog/admin.py

from django.contrib import admin
from .models import Category, Product, ProductImage, ProductVariant # ProductVariant اضافه شد
from django.utils.html import format_html

# Inline برای ProductImage (برای نمایش تصاویر در صفحه ویرایش محصول)
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1 # تعداد فیلدهای خالی برای اضافه کردن تصاویر جدید
    fields = ('image', 'is_main',) # فیلدهایی که در ادمین نمایش داده میشن

# Inline برای ProductVariant (برای نمایش گزینه‌ها در صفحه ویرایش محصول)
class ProductVariantInline(admin.TabularInline): # <--- این اضافه شد
    model = ProductVariant
    extra = 1
    fields = ('name', 'price', 'sku', 'available',) # فیلدهای واریانت

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'available', 'created_at', 'updated_at', 'category'] # <--- 'price', 'sku', 'brand' حذف شدند
    list_filter = ['available', 'created_at', 'updated_at', 'category'] # 'brand' حذف شد
    list_editable = ['available'] # <--- 'price' حذف شد
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description', 'specifications'] # 'sku', 'brand' حذف شدند
    inlines = [ProductImageInline, ProductVariantInline] # <--- ProductVariantInline اضافه شد
    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'slug', 'description', 'specifications', 'available') # 'price', 'sku', 'brand' حذف شدند
        }),
    )