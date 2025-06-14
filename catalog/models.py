from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام محصول")
    description = models.TextField(verbose_name="توضیحات و مشخصات فنی")
    sku = models.CharField(max_length=100, unique=True, verbose_name="کد یا مدل محصول")
    brand = models.CharField(max_length=100, verbose_name="برند")
    category = models.CharField(max_length=100, verbose_name="دسته‌بندی")

    STOCK_CHOICES = [
        ('AVAILABLE', 'موجود در انبار'),
        ('OUT_OF_STOCK', 'ناموجود'),
        ('COMING_SOON', 'به زودی'),
    ]
    stock_status = models.CharField(
        max_length=20,
        choices=STOCK_CHOICES,
        default='AVAILABLE',
        verbose_name="وضعیت موجودی"
    )

    image = models.ImageField(upload_to='product_images/', verbose_name="تصویر اصلی محصول")

    def __str__(self):
        return self.name
    # این کد را به انتهای فایل models.py اضافه کنید

class ProductImage(models.Model):
    # ایجاد رابطه با مدل Product. هر عکس به یک محصول تعلق دارد.
    # on_delete=models.CASCADE یعنی اگر محصول حذف شد، عکس‌هایش هم حذف شوند.
    # related_name='images' به ما اجازه می‌دهد به راحتی از یک محصول به تمام عکس‌هایش دسترسی پیدا کنیم.
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="محصول")

    # فیلد برای ذخیره خود فایل عکس
    image = models.ImageField(upload_to='product_images/gallery/', verbose_name="عکس")

    def __str__(self):
        return f"عکس برای {self.product.name}"