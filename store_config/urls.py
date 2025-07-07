from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # مسیرهای اپلیکیشن catalog
    path('', include('catalog.urls')),  

    # مسیرهای اپلیکیشن accounts
    path('accounts/', include('accounts.urls')),  
]
