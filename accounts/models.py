from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from catalog.models import Product

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
        if not extra_fields.get('is_staff'):
            raise ValueError(_('سوپروزر باید is_staff=True باشد.'))
        if not extra_fields.get('is_superuser'):
            raise ValueError(_('سوپروزر باید is_superuser=True باشد.'))
        return self.create_user(mobile_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    mobile_number = models.CharField(_('شماره موبایل'), max_length=15, unique=True)
    first_name = models.CharField(_('نام'), max_length=30, blank=True)
    last_name = models.CharField(_('نام خانوادگی'), max_length=150, blank=True)
    is_staff = models.BooleanField(_('کارمند'), default=False)
    is_active = models.BooleanField(_('فعال'), default=True)
    date_joined = models.DateTimeField(_('تاریخ عضویت'), auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.mobile_number

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', _('در انتظار پرداخت')),
        ('processing', _('در حال پردازش')),
        ('shipped', _('ارسال شده')),
        ('delivered', _('تحویل شده')),
        ('cancelled', _('لغو شده')),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name=_('کاربر'))
    order_date = models.DateTimeField(_('تاریخ سفارش'), auto_now_add=True)
    total_price = models.DecimalField(_('مبلغ کل'), max_digits=10, decimal_places=0, default=0)
    status = models.CharField(_('وضعیت سفارش'), max_length=20, choices=STATUS_CHOICES, default='pending')

    # فیلدهای اضافه‌شده برای پرداخت
    address = models.TextField(_('آدرس ارسال'), blank=True, null=True)
    phone_number = models.CharField(_('شماره تماس'), max_length=20, blank=True, null=True)
    shipping_cost = models.IntegerField(_('هزینه ارسال'), default=0)

    class Meta:
        verbose_name = _("سفارش")
        verbose_name_plural = _("سفارشات")
        ordering = ['-order_date']

    def __str__(self):
        return f"سفارش {self.id} توسط {self.user.mobile_number}"

    @property
    def get_status_display_fa(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', verbose_name=_('سفارش'), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('محصول'))
    quantity = models.PositiveIntegerField(_('تعداد'), default=1)
    price = models.DecimalField(_('قیمت واحد'), max_digits=10, decimal_places=0)

    class Meta:
        verbose_name = _("آیتم سفارش")
        verbose_name_plural = _("آیتم‌های سفارش")

    def __str__(self):
        return f"{self.quantity} x {self.product.name if self.product else _('محصول حذف شده')}"

    @property
    def total_price(self):
        return self.price * self.quantity
