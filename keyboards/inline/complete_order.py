from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

is_order_competed_callback = CallbackData("is_order_completed", "choice", "order_id")


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


