from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from data.config import OrderStatuses

orders_callback = CallbackData("orders_callback", "order_id")
orders_status_callback = CallbackData("order_status", "status")


def orders_status_markup(waiting_for_start_orders_quantity: int, in_progress_orders_quantity: int):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text=f"Подбор [{waiting_for_start_orders_quantity}]",
            callback_data=orders_status_callback.new(OrderStatuses.waiting_for_start),
        ),
        InlineKeyboardButton(
            text=f"Найден [{in_progress_orders_quantity}]",
            callback_data=orders_status_callback.new(OrderStatuses.in_progress),
        ),
    )
    return markup


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


