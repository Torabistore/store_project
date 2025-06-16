from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-(0k#6#%i=7@2%xwq8gr$z1tk!vjp(mn63abav69g#aeu293b)b'
DEBUG = True
ALLOWED_HOSTS = ['torabistore.pythonanywhere.com'] # تغییر یافته

INSTALLED_APPS = [
    'catalog.apps.CatalogConfig',
    'accounts.apps.AccountsConfig', # این خط اضافه شده و کاما تصحیح شده
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'store_config.urls'
TEMPLATES = [
    {'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [], 'APP_DIRS': True,
     'OPTIONS': {
         'context_processors': [
             'django.template.context_processors.request',
             'django.contrib.auth.context_processors.auth',
             'django.contrib.messages.context_processors.messages',
         ],
     },
    },
]
WSGI_APPLICATION = 'store_config.wsgi.application'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3',}}
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]
LANGUAGE_CODE = 'fa-ir'  # تغییر به فارسی
TIME_ZONE = 'Asia/Tehran' # تغییر منطقه زمانی
USE_I18N = True
USE_TZ = True

# --- بخش مهم فایل‌های استاتیک و مدیا ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles' # این خط اضافه شده است
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
# -----------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.User' # اضافه شده برای مدل User سفارشی

LOCALE_PATHS = [ # اضافه شده برای ترجمه
    BASE_DIR / 'locale',
]