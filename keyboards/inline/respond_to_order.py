from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

respond_callback = CallbackData("respond_to_order", "order_id")


def respond_markup(order_id: int):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="Откликнуться",
            callback_data=respond_callback.new(order_id),
        )
    )
    return markup


