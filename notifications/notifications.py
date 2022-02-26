from keyboards.inline.rating import rating_markup
from loader import bot
from keyboards.inline.respond_to_order import respond_markup
from keyboards.inline.complete_order import is_order_completed_markup
from models import OrdersModel
from data.config import OrderStatuses


async def send_message(user_telegram_id: int, text: str, reply_markup=None):
    try:
        await bot.send_message(
            chat_id=user_telegram_id,
            text=text,
            reply_markup=reply_markup
        )
    except:
        ...


async def send_voice(user_telegram_id: int, voice_file_id: str):
    try:
        await bot.send_voice(
            chat_id=user_telegram_id,
            voice=voice_file_id,
            caption="Описание задачи"
        )
    except:
        ...


async def notify_workers_about_new_order(workers: list, order: object):
    for worker in workers:
        text = f"Появилось задание!\n" \
               f"Удаленность: {worker.distance}м\n" \
               f"Имя: {order.customer_name}\n"
        if order.description:
            text += f"Задание: {order.description}"
        else:
            text += f"Категория: {order.category.name}"
        await send_message(worker.user.telegram_id, text, respond_markup(order.pk))
        if order.voice_description:
            await send_voice(worker.user.telegram_id, order.voice_description)


async def notify_worker_about_success_response(worker: object):
    ...


async def notify_worker_about_being_chosen_as_implementer(worker: object, order: object):
    text: str = ""
    if order.description:
        text = f"Вас выбрали исполнителем по заданию \"{order.description}\". Свяжитесь с заказчиком\n"
    else:
        text = f"Вас выбрали исполнителем в категории \"{order.category.name}\". Свяжитесь с заказчиком\n"
    text += "Удаленность: {вставить сюда удаленность}\n" \
            f"Имя заказчика: {order.customer_name}\n" \
            f"Задание: {order.description}\n" \
            f"Контакты: {order.customer_phone}\n"
    if order.additional_contacts:
        text += f"Дополнительные контакты: {order.additional_contacts}\n"
    if not order.allow_to_write_in_telegram:
        text += "<b>Примечание: заказчик запретил писать ему в телеграмм</b>"
    await send_message(worker.user.telegram_id, text)


async def notify_customer_about_new_response(order: object, worker: object):
    if order.description:
        text = f"На ваш заказ \"{order.description}\" откликнулся {worker.name}"
    else:
        text = f"На ваш заказ в категории {order.category.name} откликнулся {worker.name}"
    await send_message(order.customer.user.telegram_id, text)


async def notify_customer_about_completed_order(order):
    if order.description:
        text = f"Задание \"{order.description}\" выполнено?"
    else:
        text = f"Задание в категории \"{order.category.name}\" выполнено?"
    await OrdersModel.update(order.pk, status=OrderStatuses.waiting_for_finish)
    await send_message(
        user_telegram_id=order.customer.user.telegram_id,
        text=text,
        reply_markup=is_order_completed_markup(order.pk)
    )


async def notify_worker_about_completed_order(order: object):
    if order.description:
        text = f"Заказчик подтвердил выполнение задания \"{order.description}\""
    else:
        text = f"Заказчик подтвердил выполнение заказа в категории \"{order.category.name}\""
    await send_message(
        order.worker.user.telegram_id,
        text
    )
    await send_message(
        order.worker.user.telegram_id,
        "Оцените заказчика",
        rating_markup("worker", order.customer.pk, order.pk)
    )


async def notify_worker_about_new_feedback(order: object, feedback_value: int):
    if order.description:
        text = f"Вам поставили оценку {feedback_value} за задание \"{order.description}\"\n"
    else:
        text = f"Вам поставили оценку {feedback_value} за задание в категории \"{order.category.name}\"\n"
    text += f"Ваш рейтинг: {order.worker.rating}"
    await send_message(
        order.worker.user.telegram_id,
        text
    )


async def notify_customer_about_new_feedback(order: object, feedback_value: int):
    if order.description:
        text = f"Вам поставили оценку {feedback_value} за задание \"{order.description}\"\n"
    else:
        text = f"Вам поставили оченку {feedback_value} за задание в категории \"{order.category.name}\"\n"
    text += f"Ваш рейтинг: {order.customer.rating}"
    await send_message(
        order.customer.user.telegram_id,
        text
    )


