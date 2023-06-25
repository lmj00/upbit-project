from celery import shared_task
from .coin import get_ticker
import asyncio

@shared_task
def my_task():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(get_ticker())
    loop.close()


my_task.delay()