from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'  # دقیقاً همون اسم اپ
    label = 'users'  # مطمئن شو که label همون چیزی باشه که تو فایل‌ها استفاده شده
