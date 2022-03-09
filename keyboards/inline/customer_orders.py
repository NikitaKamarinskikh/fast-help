from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import callback_data
from aiogram.utils.callback_data import CallbackData
from data.config import OrderStatuses

orders_callback = CallbackData("orders_callback", "order_id", "order_status")
customer_orders_pagination_callback = CallbackData("customer_orders_pagination", "offset", "direction")
orders_status_callback = CallbackData("order_status", "status")
order_manage_callback = CallbackData("order_manage", "order_id", "option")
confirm_finish_order_callback = CallbackData("confirm_finish_order", "order_id", "choice")
find_new_candidate_callback = CallbackData("find_new_candidate", "option", "order_id")


def orders_status_markup(waiting_for_start_orders_quantity: int, in_progress_orders_quantity: int,
                         executable_quantity: int):
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
        InlineKeyboardButton(
            text=f"Выполняемые [{executable_quantity}]",
            callback_data=orders_status_callback.new("executable"),
        ),
    )
    return markup


def orders_markup(orders: list, order_satus: str, offset: int = 0, max_buttons: int = 10):
    markup = InlineKeyboardMarkup(row_width=2)
    x = 0
    for i in range(offset, len(orders)):
        if x == max_buttons:
            break
        markup.add(
            InlineKeyboardButton(
                text=f"{i + 1}. {orders[i].category.name}",
                callback_data=orders_callback.new(orders[i].pk, order_satus),
            )
        )
        x += 1

    if len(orders) > max_buttons:
        if offset != 0:
            markup.add(InlineKeyboardButton(text="<<",
                                            callback_data=customer_orders_pagination_callback.new(offset, "left")))
            if len(orders) - offset > max_buttons:
                markup.insert(InlineKeyboardButton(text=">>",
                                                   callback_data=customer_orders_pagination_callback.new(offset, "right")))
        else:
            if len(orders) > offset:
                markup.add(InlineKeyboardButton(text=">>",
                                            callback_data=customer_orders_pagination_callback.new(offset, "right")))
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


def find_new_candidate_markup(order_id: int):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="Найти нового",
            callback_data=find_new_candidate_callback.new("find_new", order_id)
        ),
        InlineKeyboardButton(
            text="Продолжить с текущим",
            callback_data=find_new_candidate_callback.new("use_current", order_id)
        )
    )
    return markup
