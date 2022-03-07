from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from keyboards.inline.respond_to_order import respond_callback

chose_payment_callback = CallbackData("chose_payment", "order_id", "distance", "amount", "with_bonus", "has_order")
payment_method_callback = CallbackData("payment_method", "method")


def chose_payment_markup(order_id: int, has_order: bool = False):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text=f"Единоразово 500м",
            callback_data=chose_payment_callback.new(order_id, 500, 30, "False", has_order),
        ),
        InlineKeyboardButton(
            text=f"Единоразово 1000м",
            callback_data=chose_payment_callback.new(order_id, 1000, 50, "False", has_order),
        ),
        InlineKeyboardButton(
            text=f"Пополнить с бонусами",
            callback_data=chose_payment_callback.new(order_id, 0, 0, "True", has_order),
        ),
    )
    return markup


def payment_method_markup(use_coins_button: bool):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text=f"Единоразово",
            callback_data=payment_method_callback.new("one_time"),
        )
    )
    if use_coins_button:
        markup.add(
            InlineKeyboardButton(
                text=f"Оплатить монетами",
                callback_data=payment_method_callback.new("coins"),
            )
        )
    markup.add(
        InlineKeyboardButton(
            text=f"Пополнить с бонусами",
            callback_data=payment_method_callback.new("with_bonus"),
        )
    )
    return markup

