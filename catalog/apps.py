from django.apps import AppConfig

class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'

    def ready(self):
        try:
            import catalog.signals  # فقط سیگنال‌هایی که وابسته به catalog.models هستن
        except ImportError as e:
            print("🚨 خطا هنگام ایمپورت سیگنال:", str(e))
