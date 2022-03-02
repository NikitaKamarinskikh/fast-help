from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from keyboards.inline.respond_to_order import respond_callback

orders_nearby_callback = CallbackData("order_nearby", "category_name", "distance")
orders_at_longer_distance_callback = CallbackData("orders_at_longer_distance", "distance")

chose_order_pagination_callback = CallbackData("chose_order_pagination", "order_id", "order_number", "direction")
back_to_orders_callback = CallbackData("back_to_orders")
confirm_show_longer_distance_orders_callback = CallbackData("confirm_show_longer_distance_orders", "choice", "distance")


def orders_nearby_markup(categories: dict, distance: int):
    markup = InlineKeyboardMarkup(row_width=2)
    for category_name, category_quantity in categories.items():
        markup.insert(
            InlineKeyboardButton(
                text=f"{category_name} ({category_quantity})",
                callback_data=orders_nearby_callback.new(category_name, distance),
            )
        )
    return markup


def orders_at_longer_distance_markup(total_1000_meters: int, total_1500_meters: int):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(
            text=f"({total_1000_meters}) 1000м",
            callback_data=orders_at_longer_distance_callback.new(1000)
        ),
        InlineKeyboardButton(
            text=f"({total_1500_meters}) 1500м",
            callback_data=orders_at_longer_distance_callback.new(1500)
        )
    )
    return markup


def chose_order_markup(order_number: int, orders_quantity: int, order_id: int):
    markup = InlineKeyboardMarkup(row_width=2)
    if orders_quantity > 1:
        if order_number < orders_quantity and order_number == 0:
            markup.add(InlineKeyboardButton(text=">>",
                                            callback_data=chose_order_pagination_callback.new(order_id,
                                                                                              order_number + 1,
                                                                                              "right")))
        elif order_number == orders_quantity - 1:
            markup.add(InlineKeyboardButton(text="<<",
                                            callback_data=chose_order_pagination_callback.new(order_id,
                                                                                              order_number - 1,
                                                                                              "left")))
        else:
            markup.add(InlineKeyboardButton(text="<<",
                                            callback_data=chose_order_pagination_callback.new(order_id,
                                                                                              order_number - 1,
                                                                                              "left")),
                       InlineKeyboardButton(text=">>",
                                            callback_data=chose_order_pagination_callback.new(order_id,
                                                                                              order_number + 1,
                                                                                              "right")))

    markup.add(
        InlineKeyboardButton(
            text="Откликнуться",
            callback_data=respond_callback.new(order_id),
        )
    )
    markup.add(
        InlineKeyboardButton(
            text="Назад",
            callback_data=back_to_orders_callback.new(),
        ),
    )
    return markup


def confirm_show_longer_distance_orders_markup(distance: int):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(
            text="Да",
            callback_data=confirm_show_longer_distance_orders_callback.new("yes", distance)
        ),
        InlineKeyboardButton(
            text="Нет",
            callback_data=confirm_show_longer_distance_orders_callback.new("no", distance)
        ),
    )
    return markup








