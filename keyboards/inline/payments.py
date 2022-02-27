from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from keyboards.inline.respond_to_order import respond_callback

chose_payment_callback = CallbackData("chose_payment", "order_id", "distance", "amount", "with_bonus")


def chose_payment_markup(order_id: int):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text=f"Единоразово 500м",
            callback_data=chose_payment_callback.new(order_id, 500, 1, "False"),
        ),
        InlineKeyboardButton(
            text=f"Единоразово 1000м",
            callback_data=chose_payment_callback.new(order_id, 1000, 1, "False"),
        ),
        InlineKeyboardButton(
            text=f"Пополнить с бонусами",
            callback_data=chose_payment_callback.new(order_id, 0, 0, "True"),
        ),
    )
    return markup


