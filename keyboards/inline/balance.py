from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

balance_callback = CallbackData("balance", "option")


def balance_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="Пополнить",
            callback_data=balance_callback.new("update_balance"),
        ),
        InlineKeyboardButton(
            text="Пригласить",
            callback_data=balance_callback.new("invite"),
        ),
    )
    return markup
