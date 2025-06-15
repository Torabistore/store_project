# accounts/models.py
from django.db import models
from django.contrib.auth.models import User # برای استفاده از مدل User پیش‌فرض جنگو
from catalog.models import Product # برای ارتباط با مدل Product شما

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="کاربر")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ سفارش")
    is_completed = models.BooleanField(default=False, verbose_name="تکمیل شده")
    total_price = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name="مبلغ کل") # قیمت را به تومان فرض می‌کنیم

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"
        ordering = ['-order_date'] # نمایش جدیدترین سفارشات در بالا

    def __str__(self):
        return f"سفارش {self.id} توسط {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="سفارش")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="محصول") # اگر محصول حذف شد، آیتم سفارش باقی بماند
    quantity = models.IntegerField(default=1, verbose_name="تعداد")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="قیمت واحد در زمان سفارش")

    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم‌های سفارش" # نام صحیح

    def __str__(self):
        return f"{self.quantity} x {self.product.name if self.product else 'محصول حذف شده'}"