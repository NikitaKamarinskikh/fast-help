from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

orders_callback = CallbackData("now", "order_id")


def orders_markup(orders: list):
    markup = InlineKeyboardMarkup(row_width=1)
    for order in orders:
        markup.add(
            InlineKeyboardButton(
                text=order.category.name,
                callback_data=orders_callback.new(order.pk),
            )
        )
    return markup


