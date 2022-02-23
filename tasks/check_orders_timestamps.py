from datetime import datetime
from time import time
from models import OrderTimestampsModel
from notifications import notify_customer_about_completed_order


async def check_orders_timestamps():
    current_time_in_seconds = int(time())
    timestamps = await OrderTimestampsModel.get_all()
    for timestamp in timestamps:
        if current_time_in_seconds >= timestamp.seconds:
            await notify_customer_about_completed_order(timestamp.order)
            await OrderTimestampsModel.delete_timestamp(timestamp)


# def set_timestamp(minutes: int) -> int:
#     return int(time.time()) + (MIN_IN_SEC * minutes)


