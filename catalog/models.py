from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe


# 🎯 دسته‌بندی محصولات
class Category(models.Model):
    name = models.CharField(_('نام دسته‌بندی'), max_length=100)
    slug = models.SlugField(_('اسلاگ'), max_length=100, unique=True)

    class Meta:
        verbose_name = _('دسته‌بندی')
        verbose_name_plural = _('دسته‌بندی‌ها')

    def __str__(self):
        return self.name


# 🧺 محصول اصلی
class Product(models.Model):
    name = models.CharField(_('نام محصول'), max_length=200)
    slug = models.SlugField(_('اسلاگ'), max_length=200, unique=True)
    description = models.TextField(_('توضیحات'), default='', blank=True)
    specifications = models.TextField(_('مشخصات'), default='', blank=True)
    price = models.DecimalField(_('قیمت پایه'), max_digits=10, decimal_places=0, default=0)
    available = models.BooleanField(_('موجود'), default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('دسته‌بندی'))
    created_at = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)
    updated_at = models.DateTimeField(_('تاریخ به‌روزرسانی'), auto_now=True)
    image_caption = models.CharField(_('توضیح زیر تصویر'), max_length=200, blank=True, default='')

    class Meta:
        verbose_name = _('محصول')
        verbose_name_plural = _('محصولات')

    def __str__(self):
        return self.name

    def formatted_price(self):
        return f"{self.price:,.0f} تومان"

    formatted_price.short_description = "قیمت (با فرمت)"


# 🖼 تصاویر محصول
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

    image_tag.short_description = "پیش‌نمایش"


# 🎨 ویژگی‌های محصول (سایز، رنگ، موجودی، قیمت نهایی)
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE, verbose_name=_('محصول'))
    color = models.CharField(_('رنگ'), max_length=50, blank=True)
    size = models.CharField(_('سایز'), max_length=50, blank=True)
    stock = models.PositiveIntegerField(_('موجودی'), default=0)
    price = models.DecimalField(_('قیمت نهایی'), max_digits=10, decimal_places=0, default=0)

    class Meta:
        verbose_name = _('ویژگی محصول')
        verbose_name_plural = _('ویژگی‌های محصول')

    def __str__(self):
        return f"{self.product.name} - {self.color} / {self.size}"


# 📝 مدل پیام‌های تماس با پشتیبانی
class ContactMessage(models.Model):
    full_name = models.CharField(_('نام و نام خانوادگی'), max_length=100)
    phone_number = models.CharField(_('شماره تماس'), max_length=20)
    message = models.TextField(_('توضیحات'))
    created_at = models.DateTimeField(_('تاریخ ارسال'), auto_now_add=True)

    class Meta:
        verbose_name = _('پیام تماس')
        verbose_name_plural = _('پیام‌های تماس')

    def __str__(self):
        return f"پیام از {self.full_name}"
