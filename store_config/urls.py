from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🔗 مسیرهای اپلیکیشن‌های پروژه
    path('', include('catalog.urls')),         # مسیر اصلی فروشگاه (صفحه‌ اصلی، محصولات، سبد خرید و ...)
    path('core/', include('core.urls')),       # مسیرهای عمومی مثل تماس با ما، پروفایل، احراز هویت
    path('users/', include('users.urls')),     # مسیرهای مربوط به مدیریت کاربران، ثبت‌نام، ورود، داشبورد و ...

    # 🗺️ فایل robots.txt
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]

# 📦 تنظیم فایل‌های static و media در حالت توسعه
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
