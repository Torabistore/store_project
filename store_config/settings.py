# settings.py

from pathlib import Path
from decouple import config 

BASE_DIR = Path(__file__).resolve().parent.parent

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# REMEMBER TO CHANGE THIS IN PRODUCTION AND KEEP IT SECRET
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
SECRET_KEY = 'django-insecure-REPLACE_THIS_WITH_YOUR_SECRET_KEY' 

DEBUG = True # <--- مطمئن شو که DEBUG=True هست

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'torabistore.pythonanywhere.com']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Your applications
    'catalog.apps.CatalogConfig',
    'accounts.apps.AccountsConfig',
    'widget_tweaks', 
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
                'catalog.context_processors.categories', 
            ],
        },
    },
]

WSGI_APPLICATION = 'store_config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_USER_MODEL = 'accounts.User' 

AUTHENTICATION_BACKENDS = [
    'accounts.backends.PhoneNumberBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'fa-ir'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static'] # <--- این خط خیلی مهمه
STATIC_ROOT = BASE_DIR / 'staticfiles' # معمولا در Production استفاده میشه، در Debug نیازی نیست بهش دست بزنی

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media' # <--- این خط خیلی مهمه

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'webmaster@localhost'

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

SMS_API_KEY = config('SMS_API_KEY')
SMS_SENDER_NUMBER = config('SMS_SENDER_NUMBER')