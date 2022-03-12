from datetime import datetime
from time import time
from models import OrderTimestampsModel
from notifications import notify_customer_about_completed_order


async def check_orders_timestamps():
    current_time_in_seconds = int(datetime.today().timestamp())
    timestamps = await OrderTimestampsModel.get_all()
    for timestamp in timestamps:
        if current_time_in_seconds >= timestamp.seconds:
            await notify_customer_about_completed_order(timestamp.order)
            await OrderTimestampsModel.delete_timestamp(timestamp)




