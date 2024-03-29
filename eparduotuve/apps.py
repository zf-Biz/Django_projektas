from django.apps import AppConfig


class EparduotuveConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eparduotuve'

    def ready(self):
        from .signals import create_profile, save_profile
