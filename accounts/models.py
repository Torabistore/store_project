# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _ # برای ترجمه متون
from catalog.models import Product # برای ارتباط با مدل Product شما (اگر از آن استفاده می کنید)

# مدیر سفارشی برای مدل User
class CustomUserManager(BaseUserManager):
    def create_user(self, mobile_number, password=None, **extra_fields):
        if not mobile_number:
            raise ValueError(_('شماره موبایل برای ایجاد کاربر الزامی است.')) # ترجمه شد
        user = self.model(mobile_number=mobile_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.')) # ترجمه شد
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.')) # ترجمه شد
        return self.create_user(mobile_number, password, **extra_fields)

# مدل User سفارشی
class User(AbstractBaseUser, PermissionsMixin):
    mobile_number = models.CharField(_('شماره موبایل'), max_length=15, unique=True) # ترجمه شد
    first_name = models.CharField(_('نام'), max_length=30, blank=True) # ترجمه شد
    last_name = models.CharField(_('نام خانوادگی'), max_length=150, blank=True) # ترجمه شد
    is_staff = models.BooleanField(_('کارمند'), default=False) # ترجمه شد
    is_active = models.BooleanField(_('فعال'), default=True) # ترجمه شد
    date_joined = models.DateTimeField(_('تاریخ عضویت'), auto_now_add=True) # ترجمه شد

    objects = CustomUserManager()

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران') # اضافه شد

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.mobile_number

# مدل‌های ساده برای Order و OrderItem (مانند قبل، اما با اصلاحات لازم)
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name=_('کاربر')) # related_name و ترجمه اضافه شد
    order_date = models.DateTimeField(_('تاریخ سفارش'), auto_now_add=True) # ترجمه شد
    is_completed = models.BooleanField(_('تکمیل شده'), default=False) # ترجمه شد
    total_price = models.DecimalField(_('مبلغ کل'), max_digits=10, decimal_places=0, default=0) # فیلد واقعی برای قیمت کل

    class Meta:
        verbose_name = _("سفارش") # ترجمه شد
        verbose_name_plural = _("سفارشات") # اضافه شد
        ordering = ['-order_date']

    def __str__(self):
        return f"سفارش {self.id} توسط {self.user.mobile_number}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', verbose_name=_('سفارش'), on_delete=models.CASCADE) # ترجمه شد
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('محصول')) # product اضافه شد، null=True, blank=True
    quantity = models.PositiveIntegerField(_('تعداد'), default=1) # ترجمه شد
    price = models.DecimalField(_('قیمت واحد'), max_digits=10, decimal_places=0) # فیلد واقعی برای قیمت واحد

    class Meta:
        verbose_name = _("آیتم سفارش") # ترجمه شد
        verbose_name_plural = _("آیتم‌های سفارش") # اضافه شد

    def __str__(self):
        return f"{self.quantity} x {self.product.name if self.product else _('محصول حذف شده')}" # ترجمه شد