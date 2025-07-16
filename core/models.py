from django.db import models
from django.conf import settings  # برای AUTH_USER_MODEL
# from users.models import Address


# ✅ محصول
class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام محصول')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    price = models.PositiveIntegerField(verbose_name='قیمت (تومان)')
    created_at = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# ✅ تصاویر محصول
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', verbose_name='تصویر محصول')

    def __str__(self):
        return f"تصویر {self.product.name}"

# ✅ سفارش
class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='کاربر',
        related_name='core_orders'  # ✅ رفع برخورد با catalog.Order
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت سفارش')
    total_price = models.PositiveIntegerField(verbose_name='مبلغ کل سفارش')

    def __str__(self):
        return f"سفارش #{self.id} برای {self.user}"

# ✅ آیتم‌های سفارش
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField(verbose_name='قیمت واحد')

    def __str__(self):
        return f"{self.quantity} عدد {self.product.name} در سفارش #{self.order.id}"

# ✅ درخواست پرداخت بدهی - نسخه core
class PaymentRequest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='کاربر',
        related_name='core_payment_requests'  # ← این خط اضافه شد برای رفع برخورد
    )
    amount = models.PositiveIntegerField(verbose_name='مبلغ پرداختی')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    payment_receipt = models.ImageField(upload_to='receipts/', verbose_name='تصویر فیش پرداخت')
    reference_number = models.CharField(max_length=100, blank=True, verbose_name='شماره پیگیری')
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'در انتظار'),
            ('approved', 'تأیید شده'),
            ('rejected', 'رد شده')
        ],
        default='pending',
        verbose_name='وضعیت بررسی'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت درخواست')

    def __str__(self):
        return f"{self.user.username} - {self.amount} تومان"

# ✅ آیتم‌های سبد خرید
class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان افزودن')

    def __str__(self):
        return f"{self.user.username} - {self.quantity} عدد {self.product.name}"
