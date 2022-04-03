from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

balance_callback = CallbackData("balance", "option")
coins_sum_callback = CallbackData("coins_sum", "coins", "amount_rub")


def balance_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="Пополнить",
            callback_data=balance_callback.new("update_balance"),
        )
        # InlineKeyboardButton(
        #     text="Пригласить",
        #     callback_data=balance_callback.new("invite"),
        # ),
    )
    return markup


def coins_sum_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="110 монет - 100р",
            callback_data=coins_sum_callback.new(110, 100),
        ),
        InlineKeyboardButton(
            text="230 монет - 200р",
            callback_data=coins_sum_callback.new(230, 200),
        ),
        InlineKeyboardButton(
            text="600 монет - 500р",
            callback_data=coins_sum_callback.new(600, 500),
        ),
        InlineKeyboardButton(
            text="1250 монет - 1000р",
            callback_data=coins_sum_callback.new(1250, 1000),
        ),
    )
    return markup


