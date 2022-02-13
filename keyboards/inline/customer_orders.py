from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

orders_callback = CallbackData("now", "order_id")


def orders_markup(orders: list):
    markup = InlineKeyboardMarkup(row_width=1)
    for order in enumerate(orders):
        markup.add(
            InlineKeyboardButton(
                text=f"{order[0] + 1}. {order[1].category.name}",
                callback_data=orders_callback.new(order[1].pk),
            )
        )
    return markup


