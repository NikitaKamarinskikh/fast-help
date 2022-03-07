from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

executable_orders_pagination_callback = CallbackData("candidate_pagination", "order_id", "order_number", "direction")


def executable_orders_markup(order_id: int, order_number: int, orders_quantity: int):
    markup = InlineKeyboardMarkup(row_width=2)
    if orders_quantity > 1:
        if order_number < orders_quantity and order_number == 0:
            markup.add(InlineKeyboardButton(text=">>",
                                            callback_data=executable_orders_pagination_callback.new(order_id,
                                                                                                    order_number + 1,
                                                                                                    "right")))
        elif order_number == orders_quantity - 1:
            markup.add(InlineKeyboardButton(text="<<",
                                            callback_data=executable_orders_pagination_callback.new(order_id,
                                                                                                    order_number - 1,
                                                                                                    "left")))
        else:
            markup.add(InlineKeyboardButton(text="<<",
                                            callback_data=executable_orders_pagination_callback.new(order_id,
                                                                                                    order_number - 1,
                                                                                                    "left")),
                       InlineKeyboardButton(text=">>",
                                            callback_data=executable_orders_pagination_callback.new(order_id,
                                                                                                    order_number + 1,
                                                                                                    "right")))
    return markup



