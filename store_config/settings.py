import os
from pathlib import Path
from decouple import config
from django.contrib.messages import constants as messages

# 🗂 مسیر پایه پروژه
BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 امنیت
SECRET_KEY = config('SECRET_KEY', default='django-insecure-فقط-برای-تست')

DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(',')

# 📦 اپلیکیشن‌ها
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'widget_tweaks',
    'admin_interface',
    'colorfield',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'crispy_forms',
    'crispy_bootstrap4',

    # اپ‌های خودت 👇
    'core',
    'catalog',
    'users',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# ⚙️ میان‌افزارها
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 🌐 مسیرهای اصلی پروژه
ROOT_URLCONF = 'store_config.urls'
WSGI_APPLICATION = 'store_config.wsgi.application'

# 🎨 قالب‌ها
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 🗃 پایگاه داده SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 👤 احراز هویت سفارشی
AUTH_USER_MODEL = 'users.CustomUser'
LOGIN_REDIRECT_URL = 'catalog:profile'
LOGOUT_REDIRECT_URL = 'catalog:homepage'
LOGIN_URL = '/login/'

# 🔐 سیاست رمز عبور
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 6}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
]

# 🌍 تنظیمات بین‌المللی
LANGUAGE_CODE = 'fa'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True

# 🎨 فایل‌های استاتیک و مدیا
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ✉️ پیام‌ها
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    messages.SUCCESS: 'success',
    messages.INFO: 'info',
    messages.WARNING: 'warning',
}

# 📬 ایمیل و پیامک
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@example.com')

SMS_API_KEY = config('SMS_API_KEY', default='API_KEY_TEST')
SMS_SENDER_NUMBER = config('SMS_SENDER_NUMBER', default='0000000000')
