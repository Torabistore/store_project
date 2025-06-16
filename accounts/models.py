# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _ # برای ترجمه متون
from catalog.models import Product

# Manager برای مدل User سفارشی
class CustomUserManager(BaseUserManager):
    def create_user(self, mobile_number, password=None, **extra_fields):
        if not mobile_number:
            raise ValueError(_('شماره موبایل برای ایجاد کاربر الزامی است.'))
        user = self.model(mobile_number=mobile_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(mobile_number, password, **extra_fields)

# مدل User سفارشی
class User(AbstractBaseUser, PermissionsMixin):
    mobile_number = models.CharField(_('شماره موبایل'), max_length=15, unique=True)
    first_name = models.CharField(_('نام'), max_length=30, blank=True)
    last_name = models.CharField(_('نام خانوادگی'), max_length=30, blank=True)
    is_active = models.BooleanField(_('فعال'), default=True)
    is_staff = models.BooleanField(_('کارمند'), default=False)
    date_joined = models.DateTimeField(_('تاریخ عضویت'), auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'mobile_number' # تنظیم شماره موبایل به عنوان فیلد نام کاربری
    REQUIRED_FIELDS = ['first_name', 'last_name'] # فیلدهای الزامی هنگام ایجاد Superuser

    class Meta:
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.mobile_number

# مدل‌های Order و OrderItem (همان‌هایی که قبلاً داشتیم)
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="کاربر") # اینجا به مدل User جدید اشاره می‌کند
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ سفارش")
    is_completed = models.BooleanField(default=False, verbose_name="تکمیل شده")
    total_price = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name="مبلغ کل") # قیمت را به تومان فرض می‌کنیم

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"
        ordering = ['-order_date'] # نمایش جدیدترین سفارشات در بالا

    def __str__(self):
        return f"سفارش {self.id} توسط {self.user.mobile_number}" # تغییر به mobile_number

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="سفارش")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="محصول")
    quantity = models.IntegerField(default=1, verbose_name="تعداد")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="قیمت واحد در زمان سفارش")

    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم‌های سفارش" # تصحیح نام verbose_plural

    def __str__(self):
        return f"{self.quantity} x {self.product.name if self.product else 'محصول حذف شده'}"