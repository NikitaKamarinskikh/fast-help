from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

update_order_start_date_callback = CallbackData("_now")
update_order_execution_time_callback = CallbackData("order_execution_time", "time", "order_id")


def update_order_start_date_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="Сейчас",
            callback_data=update_order_start_date_callback.new(),
        )
    )
    return markup


def update_order_execution_time_markup(order_id: int):
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(
        InlineKeyboardButton(
            text="10 мин",
            callback_data=update_order_execution_time_callback.new("00-10", order_id),
        ),
        InlineKeyboardButton(
            text="15 мин",
            callback_data=update_order_execution_time_callback.new("00-15", order_id),
        ),
        InlineKeyboardButton(
            text="30 мин",
            callback_data=update_order_execution_time_callback.new("00-30", order_id),
        ),
        InlineKeyboardButton(
            text="1 час",
            callback_data=update_order_execution_time_callback.new("00-59", order_id),
        ),
        InlineKeyboardButton(
            text="2 часа",
            callback_data=update_order_execution_time_callback.new("2-00", order_id),
        ),
        InlineKeyboardButton(
            text="3 часа",
            callback_data=update_order_execution_time_callback.new("3-00", order_id),
        ),
        InlineKeyboardButton(
            text="6 часов",
            callback_data=update_order_execution_time_callback.new("6-00", order_id),
        ),
        InlineKeyboardButton(
            text="12 часов",
            callback_data=update_order_execution_time_callback.new("12-00", order_id),
        ),
        InlineKeyboardButton(
            text="24 часа",
            callback_data=update_order_execution_time_callback.new("23-59", order_id),
        ),
    )
    return markup





