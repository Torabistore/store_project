# store_config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),
    path('accounts/', include('accounts.urls')), 
]

# <--- این بخش برای سرو کردن فایل‌های Static و Media در محیط توسعه اضافه شد
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # <--- این خط اضافه شد (برای اطمینان از سرو Static)
# <--- پایان بخش اضافه شده