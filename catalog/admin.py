from django.contrib import admin
from django.utils.html import mark_safe # این را برای نمایش پیش‌نمایش عکس وارد می‌کنیم
from .models import Product, ProductImage # مدل ProductImage را هم وارد می‌کنیم

# این کلاس جدید برای نمایش فرم آپلود عکس‌ها در صفحه محصول است
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # به صورت پیش‌فرض، یک فیلد خالی برای آپلود عکس جدید نشان می‌دهد
    readonly_fields = ('image_preview',) # یک فیلد فقط خواندنی برای پیش‌نمایش عکس

    # این تابع یک تگ img برای نمایش عکس در پنل ادمین می‌سازد
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" />')
        return ""
    image_preview.short_description = 'پیش‌نمایش عکس'


# این کلاس ProductAdmin قبلی ماست که آن را ویرایش می‌کنیم
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'stock_status')
    list_filter = ('category', 'brand', 'stock_status')
    search_fields = ('name', 'sku', 'brand')
    fieldsets = (
        (None, {'fields': ('name', 'sku', 'image')}), # 'image' عکس اصلی محصول است
        ('مشخصات', {'fields': ('brand', 'category', 'description')}),
        ('انبارداری', {'fields': ('stock_status',)}),
    )

    # این خط جدید، بخش مدیریت گالری تصاویر را به صفحه ویرایش محصول اضافه می‌کند
    inlines = [ProductImageInline]


# ما دیگر به این خط نیاز نداریم چون از دکوراتور @admin.register استفاده کردیم
# admin.site.register(ProductImage)