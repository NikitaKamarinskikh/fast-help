import aioschedule
from asyncio import sleep

from .check_orders_timestamps import check_orders_timestamps


async def setup():
    aioschedule.every().minute.do(check_orders_timestamps)

    while True:
        await aioschedule.run_pending()
        await sleep(1)


