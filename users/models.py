
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class CustomUserManager(BaseUserManager): # type: ignore
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

class CustomUser(AbstractBaseUser, PermissionsMixin): # type: ignore
    first_name = models.CharField(max_length=30, verbose_name='نام')
    last_name = models.CharField(max_length=30, verbose_name='نام خانوادگی')
    phone_number = models.CharField(max_length=11, unique=True, verbose_name='شماره همراه')
    email = models.EmailField(blank=True, verbose_name='ایمیل')
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True, verbose_name='تصویر پروفایل')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
         return f"{self.first_name} {self.last_name} - {self.phone_number}"



# ✅ مدل آدرس کاربر
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')
    address_line = models.TextField(verbose_name='نشانی کامل')
    city = models.CharField(max_length=100, verbose_name='شهر')
    postal_code = models.CharField(max_length=20, verbose_name='کد پستی')
    phone = models.CharField(max_length=15, verbose_name='شماره تماس')
    created_at = models.DateTimeField(auto_now_add=True)

    