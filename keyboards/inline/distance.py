from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from data.config import distances
order_distance_callback = CallbackData("order_distance", "distance")


def order_distance_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text=f"{distances.short.meters}м",
            callback_data=order_distance_callback.new(distances.short.meters),
        ),
        InlineKeyboardButton(
            text=f"{distances.middle.meters}м",
            callback_data=order_distance_callback.new(distances.middle.meters),
        ),
    )
    return markup

