from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Developer 2 : register login/logout audit signal handlers
        from . import signals  # noqa: F401
