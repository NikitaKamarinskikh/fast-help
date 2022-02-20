from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

orders_nearby_callback = CallbackData("order_nearby", "category_name", "order_id")
orders_at_longer_distance_callback = CallbackData("orders_at_longer_distance", "distance")

chose_order_callback = CallbackData("chose_order", "order_id")
chose_order_pagination_callback = CallbackData("chose_order_pagination", "order_id", "order_number", "direction")
back_to_orders_callback = CallbackData("back_to_orders")


def orders_nearby_markup(categories: dict):
    markup = InlineKeyboardMarkup(row_width=2)
    for category_id, category_data in categories.items():
        markup.insert(
            InlineKeyboardButton(
                text=f"{category_data.get('name')} ({category_data.get('quantity')})",
                callback_data=orders_nearby_callback.new(category_data.get('name'), category_data.get('order_id')),
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
            callback_data=chose_order_callback.new(order_id),
        )
    )
    markup.add(
        InlineKeyboardButton(
            text="Назад",
            callback_data=back_to_orders_callback.new(),
        ),
    )
    return markup
