from django.db import models
from django.urls import reverse
from django.db.models import Index

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name='نام دسته')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='اسلاگ')
    description = models.TextField(blank=True, verbose_name='توضیحات دسته')

    class Meta:
        ordering = ('name',)
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def get_absolute_url(self):
        return reverse('catalog:category_products', args=[self.slug])

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name='دسته بندی')
    name = models.CharField(max_length=200, db_index=True, verbose_name='نام محصول')
    slug = models.SlugField(max_length=200, db_index=True, unique=True, verbose_name='اسلاگ')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    
    # <--- این خط قبلا کامنت بود و برای رفع خطای NOT NULL constraint failed فعال شد --->
    # این فیلد اختیاری است چون قیمت اصلی می‌تواند از Variantها گرفته شود.
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=0, 
        blank=True,      # اجازه می‌دهد فیلد خالی باشد
        null=True,       # اجازه می‌دهد در دیتابیس NULL باشد
        verbose_name='قیمت اصلی (تومان)' # نام واضح‌تر
    ) 

    available = models.BooleanField(default=True, verbose_name='موجود است')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    specifications = models.TextField(blank=True, null=True, verbose_name="مشخصات محصول (هر خط یک مشخصه)")
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        indexes = [
            Index(fields=['id', 'slug']),
        ]

    def get_absolute_url(self):
        return reverse('catalog:product_detail', args=[self.id]) # or pk=self.pk if you use pk in urls.py

    def __str__(self):
        return self.name

# =========== مدل ProductVariant برای گزینه‌های محصول ===========
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE, verbose_name='محصول اصلی')
    name = models.CharField(max_length=100, verbose_name='نام گزینه (مثلاً بشقاب برنج)')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='قیمت این گزینه (تومان)')
    sku = models.CharField(max_length=50, blank=True, verbose_name='کد کالا (SKU)')
    available = models.BooleanField(default=True, verbose_name='موجود است')
    
    class Meta:
        verbose_name = 'گزینه محصول'
        verbose_name_plural = 'گزینه‌های محصول'
        unique_together = ('product', 'name')

    def __str__(self):
        return f"{self.product.name} - {self.name}"

# =========== مدل ProductImage برای گالری تصاویر محصول ===========
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE, verbose_name='محصول')
    image = models.ImageField(upload_to='products/gallery/%Y/%m/%d', verbose_name='تصویر')
    is_main = models.BooleanField(default=False, verbose_name='تصویر اصلی') 

    class Meta:
        verbose_name = 'تصویر محصول'
        verbose_name_plural = 'تصاویر محصولات'
        ordering = ['is_main', 'id'] 

    def __str__(self):
        return f"تصویر {self.id} برای {self.product.name}"