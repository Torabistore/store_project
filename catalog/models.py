from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe


class Category(models.Model):
    name = models.CharField(_('نام دسته‌بندی'), max_length=100)
    slug = models.SlugField(_('اسلاگ'), max_length=100, unique=True)

    class Meta:
        verbose_name = _('دسته‌بندی')
        verbose_name_plural = _('دسته‌بندی‌ها')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(_('نام محصول'), max_length=200)
    slug = models.SlugField(_('اسلاگ'), max_length=200, unique=True)
    description = models.TextField(_('توضیحات'), default='', blank=True)
    specifications = models.TextField(_('مشخصات'), default='', blank=True)
    price = models.DecimalField(_('قیمت'), max_digits=10, decimal_places=0, default=0)
    available = models.BooleanField(_('موجود'), default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('دسته‌بندی'))
    created_at = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)
    updated_at = models.DateTimeField(_('تاریخ به‌روزرسانی'), auto_now=True)

    class Meta:
        verbose_name = _('محصول')
        verbose_name_plural = _('محصولات')

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE, verbose_name=_('محصول'))
    image = models.ImageField(_('تصویر'), upload_to='products/')
    is_main = models.BooleanField(_('تصویر اصلی'), default=False)

    class Meta:
        verbose_name = _('تصویر محصول')
        verbose_name_plural = _('تصاویر محصول')

    def __str__(self):
        return f"تصویر برای {self.product.name}"

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="100" />')
        return "No Image"

    image_tag.short_description = "پیش‌نمایش"  # ✅ اضافه کن برای نمایش در admin
