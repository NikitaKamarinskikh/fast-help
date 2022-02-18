from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from data.config import OrderStatuses

orders_callback = CallbackData("orders_callback", "order_id", "order_status")
orders_status_callback = CallbackData("order_status", "status")
order_manage_callback = CallbackData("order_manage", "order_id", "option")
confirm_finish_order_callback = CallbackData("confirm_finish_order", "order_id", "choice")


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


def orders_markup(orders: list, order_satus: str):
    markup = InlineKeyboardMarkup(row_width=1)
    for order in enumerate(orders):
        markup.add(
            InlineKeyboardButton(
                text=f"{order[0] + 1}. {order[1].category.name}",
                callback_data=orders_callback.new(order[1].pk, order_satus),
            )
        )
    return markup


def order_manage_markup(order_id: int):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="Завершить",
            callback_data=order_manage_callback.new(order_id, "finish")
        ),
        InlineKeyboardButton(
            text="Повторный поиск",
            callback_data=order_manage_callback.new(order_id, "find_new_candidate")
        )
    )
    return markup


def confirm_finish_order_markup(order_id: int):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="Завершить",
            callback_data=confirm_finish_order_callback.new(order_id, "yes")
        ),
        InlineKeyboardButton(
            text="Отмена",
            callback_data=confirm_finish_order_callback.new(order_id, "no")
        )
    )
    return markup



