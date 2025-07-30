from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Import signals to register them
        import core.signals
        try:
            from django.contrib.sites.models import Site
            from .models import create_default_site
            create_default_site()
        except:
            pass  