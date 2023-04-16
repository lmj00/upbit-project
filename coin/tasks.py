from background_task import background
from .coin import get_ticker
from datetime import datetime

import asyncio


@background(schedule=datetime.now())
def background_ticker():
    asyncio.run(get_ticker())