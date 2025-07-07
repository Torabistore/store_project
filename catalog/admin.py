from django.contrib import admin
from .models import Category, Product, ProductImage
from django.utils.html import format_html

# Inline برای ProductImage (برای نمایش تصاویر در صفحه ویرایش محصول)
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # تعداد فیلدهای خالی برای اضافه کردن تصاویر جدید
    fields = ('image', 'is_main')  # فیلدهایی که در ادمین نمایش داده میشن

    def image_tag(self, obj):
        return format_html('<img src="{}" style="width: 100px; height: 100px;" />'.format(obj.image.url))
    
    image_tag.short_description = 'تصویر'

    # اضافه کردن تصویر در فیلدهای inline
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj:
            fields += ('image_tag',)
        return fields

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
    inlines = [ProductImageInline]  # فقط ProductImageInline
    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'slug', 'description', 'specifications', 'available')
        }),
    )

    # نمایش تصویر اصلی در لیست محصولات
    def main_image_tag(self, obj):
        if obj.images.exists():
            return format_html('<img src="{}" style="width: 100px; height: 100px;" />'.format(obj.images.first().image.url))
        return '-'
    
    main_image_tag.short_description = 'تصویر اصلی'

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image']
    list_filter = ['product']