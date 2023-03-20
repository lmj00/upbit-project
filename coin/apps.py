from django.apps import AppConfig


class CoinConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coin'
    
    def ready(self):
        from coin.price import get_ticker
        import asyncio
        asyncio.run(get_ticker())