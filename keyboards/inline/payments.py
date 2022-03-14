from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data.config import distances, PaymentMethods
from keyboards.inline.respond_to_order import respond_callback

chose_payment_callback = CallbackData("chose_payment", "order_id", "distance", "amount", "with_bonus", "has_order")
payment_method_callback = CallbackData("payment_method", "method")


def chose_payment_markup(order_id: int, has_order: bool = False):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text=f"Единоразово {distances.short.meters}м",
            callback_data=chose_payment_callback.new(order_id, distances.short.meters, distances.short.customer_price,
                                                     "False", has_order),
        ),
        InlineKeyboardButton(
            text=f"Единоразово 1000м",
            callback_data=chose_payment_callback.new(order_id, distances.middle.meters, distances.middle.customer_price,
                                                     "False", has_order),
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
            callback_data=payment_method_callback.new(PaymentMethods.one_time),
        )
    )
    if use_coins_button:
        markup.add(
            InlineKeyboardButton(
                text=f"Оплатить монетами",
                callback_data=payment_method_callback.new(PaymentMethods.coins),
            )
        )
    markup.add(
        InlineKeyboardButton(
            text=f"Пополнить с бонусами",
            callback_data=payment_method_callback.new(PaymentMethods.with_bonus),
        )
    )
    return markup

