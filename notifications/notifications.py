from loader import bot
from keyboards.inline.respond_to_order import respond_markup


async def send_message(user_telegram_id: int, text: str, reply_markup=None):
    try:
        await bot.send_message(
            chat_id=user_telegram_id,
            text=text,
            reply_markup=reply_markup
        )
    except:
        ...


async def notify_workers_about_new_order(workers_data: list, order: object):
    for worker_data in workers_data:
        worker = worker_data.get("worker")
        text = f"Появилось задание!\n" \
               f"Удаленность: {worker_data.get('distance')}м\n" \
               f"Имя: {order.customer_name}\n"
        if order.description:
            text += f"Задание: {order.description}"
        else:
            text += f"Категория: {order.category.name}"
        await send_message(worker.user.telegram_id, text, respond_markup(order.pk))


async def notify_worker_about_success_response(worker: object):
    ...


async def notify_worker_about_being_chosen_as_implementer(customer: object, worker: object, order: object):
    ...


async def notify_customer_about_new_response(order: object, worker: object):
    if order.description:
        text = f"На ваш заказ {order.description} откликнулся {worker.name}"
    else:
        text = f"На ваш заказ в категории {order.category.name} откликнулся {worker.name}"
    await send_message(order.customer.user.telegram_id, text)















