from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# 🔧 مدیریت کاربران سفارشی
class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("شماره همراه الزامی است")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)


# 👤 مدل اصلی کاربر
class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('نام'), max_length=30)
    last_name = models.CharField(_('نام خانوادگی'), max_length=30)
    phone_number = models.CharField(_('شماره همراه'), max_length=11, unique=True)
    email = models.EmailField(_('ایمیل'), blank=True)
    profile_image = models.ImageField(_('تصویر پروفایل'), upload_to='profile_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.phone_number}"


# 📇 پروفایل کاربر
class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('کاربر')
    )
    bio = models.TextField(_('بیوگرافی'), blank=True)
    birth_date = models.DateField(_('تاریخ تولد'), blank=True, null=True)
    avatar = models.ImageField(_('آواتار'), upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)
    updated_at = models.DateTimeField(_('آخرین بروزرسانی'), auto_now=True)

    class Meta:
        verbose_name = _('پروفایل کاربر')
        verbose_name_plural = _('پروفایل‌های کاربران')
        ordering = ['-created_at']

    def __str__(self):
        return f"پروفایل {self.user.phone_number}"


# 🏠 آدرس کاربر
class Address(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('کاربر')
    )
    address_line = models.TextField(_('نشانی کامل'))
    city = models.CharField(_('شهر'), max_length=100)
    postal_code = models.CharField(_('کد پستی'), max_length=20)
    phone = models.CharField(_('شماره تماس'), max_length=15)
    created_at = models.DateTimeField(_('تاریخ ثبت'), auto_now_add=True)

    class Meta:
        verbose_name = _('آدرس')
        verbose_name_plural = _('آدرس‌ها')
        ordering = ['-created_at']

    def __str__(self):
        return f"آدرس برای {self.user.phone_number}"
