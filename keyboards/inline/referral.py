from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

referral_callback = CallbackData("referral", "option")


def referral_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="Получить ссылку",
            callback_data=referral_callback.new("get_link"),
        ),
        InlineKeyboardButton(
            text="Назад",
            callback_data=referral_callback.new("back"),
        ),
    )
    return markup


