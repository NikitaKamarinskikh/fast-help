from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

order_execution_time_callback = CallbackData("order_execution_time", "time_in_minutes")


def order_execution_time_markup():
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(
        InlineKeyboardButton(
            text="10 мин",
            callback_data=order_execution_time_callback.new(10),
        ),
        InlineKeyboardButton(
            text="15 мин",
            callback_data=order_execution_time_callback.new(12),
        ),
        InlineKeyboardButton(
            text="30 мин",
            callback_data=order_execution_time_callback.new(30),
        ),
        InlineKeyboardButton(
            text="1 час",
            callback_data=order_execution_time_callback.new(60),
        ),
        InlineKeyboardButton(
            text="2 часа",
            callback_data=order_execution_time_callback.new(120),
        ),
        InlineKeyboardButton(
            text="3 часа",
            callback_data=order_execution_time_callback.new(180),
        ),
        InlineKeyboardButton(
            text="6 часов",
            callback_data=order_execution_time_callback.new(360),
        ),
        InlineKeyboardButton(
            text="12 часов",
            callback_data=order_execution_time_callback.new(720),
        ),
        InlineKeyboardButton(
            text="24 часа",
            callback_data=order_execution_time_callback.new(1440),
        ),
    )
    return markup
