from django.apps import AppConfig


class CoinConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coin'

    def ready(self):
        from .tasks import background_ticker
        background_ticker()