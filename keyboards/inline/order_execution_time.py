from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

order_execution_time_callback = CallbackData("order_execution_time", "time")


def order_execution_time_markup():
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(
        InlineKeyboardButton(
            text="10 мин",
            callback_data=order_execution_time_callback.new("00-10"),
        ),
        InlineKeyboardButton(
            text="15 мин",
            callback_data=order_execution_time_callback.new("00-15"),
        ),
        InlineKeyboardButton(
            text="30 мин",
            callback_data=order_execution_time_callback.new("00-30"),
        ),
        InlineKeyboardButton(
            text="1 час",
            callback_data=order_execution_time_callback.new("00-60"),
        ),
        InlineKeyboardButton(
            text="2 часа",
            callback_data=order_execution_time_callback.new("2-00"),
        ),
        InlineKeyboardButton(
            text="3 часа",
            callback_data=order_execution_time_callback.new("3-00"),
        ),
        InlineKeyboardButton(
            text="6 часов",
            callback_data=order_execution_time_callback.new("6-00"),
        ),
        InlineKeyboardButton(
            text="12 часов",
            callback_data=order_execution_time_callback.new("12-00"),
        ),
        InlineKeyboardButton(
            text="24 часа",
            callback_data=order_execution_time_callback.new("24-00"),
        ),
    )
    return markup
