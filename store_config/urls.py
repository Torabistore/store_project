from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views
from core.views import confirm_payment_view
from users.views import CustomLoginView
urlpatterns = [
    # 🔐 مدیریت Django
    path('admin/', admin.site.urls),

    path('', include('core.urls')),       # برای صفحه اصلی
    path('product/', include('catalog.urls')),  # برای محصولات

    path('confirm-payment/<int:id>/', confirm_payment_view, name='confirm_payment'),

    # 🔐 مسیر جایگزین برای accounts
     path('accounts/login/', CustomLoginView.as_view(), name='login_alias')
    
]

# ⚙️ استاتیک و مدیا
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

