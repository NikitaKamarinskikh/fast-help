from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

order_distance_callback = CallbackData("order_distance", "distance")


def order_distance_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="500м",
            callback_data=order_distance_callback.new(500),
        ),
        InlineKeyboardButton(
            text="1000м",
            callback_data=order_distance_callback.new(1000),
        ),
    )
    return markup

