from loader import bot


async def send_message(user_telegram_id: int, text: str):
    try:
        await bot.send_message(
            chat_id=user_telegram_id,
            text=text
        )
    except:
        ...


async def notify_worker_about_new_order(worker: object, order: object):
    ...


async def notify_worker_about_success_response(worker: object):
    ...


async def notify_worker_about_being_chosen_as_implementer(customer: object, worker: object, order: object):
    ...


async def notify_customer_about_new_response(customer: object, worker: object, order: object):
    ...














