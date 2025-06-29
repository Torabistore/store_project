# catalog/admin.py

from django.contrib import admin
from .models import Category, Product, ProductImage # <--- ProductImage هم import شد

# Inline برای ProductImage (برای نمایش تصاویر در صفحه ویرایش محصول)
class ProductImageInline(admin.TabularInline): # یا admin.StackedInline
    model = ProductImage
    extra = 1 # تعداد فیلدهای خالی برای اضافه کردن تصاویر جدید
    fields = ('image', 'is_main',) # فیلدهایی که در ادمین نمایش داده میشن

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)} # slug را بر اساس name پر می کند

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created_at', 'updated_at']
    list_filter = ['available', 'created_at', 'updated_at', 'category']
    list_editable = ['price', 'available'] # این فیلدها را می توان مستقیم از لیست ویرایش کرد
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline] # <--- ProductImageInline به ProductAdmin اضافه شد