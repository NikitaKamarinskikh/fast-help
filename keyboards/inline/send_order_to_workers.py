from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

send_order_to_workers_callback = CallbackData("send_order", "order_id", "distance")


def send_order_to_workers_markup(order_id: int, distance: int):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="Отправить задания исполнителям",
            callback_data=send_order_to_workers_callback.new(order_id, distance),
        )
    )
    return markup




