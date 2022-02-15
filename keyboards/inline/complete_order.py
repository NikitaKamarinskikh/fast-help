from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

is_order_competed_callback = CallbackData("is_order_completed", "choice", "order_id")
order_complete_denied_callback = CallbackData("order_denied", "action", "worker_id", "order_id")


def is_order_completed_markup(order_id: int):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="Да",
            callback_data=is_order_competed_callback.new("yes", order_id)
        ),
        InlineKeyboardButton(
            text="Нет",
            callback_data=is_order_competed_callback.new("no", order_id)
        )
    )
    return markup


def order_complete_denied_markup(order_id: int, worker_id: int):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="Добавить время",
            callback_data=order_complete_denied_callback.new("add_time", order_id, worker_id)
        ),
        InlineKeyboardButton(
            text="Найти нового",
            callback_data=order_complete_denied_callback.new("find_new_candidate", order_id, worker_id)
        )
    )
    return markup


