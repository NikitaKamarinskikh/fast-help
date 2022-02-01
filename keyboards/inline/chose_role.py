from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from data.config import Roles

chose_role_callback = CallbackData('chose_role', 'role')


def chose_role_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="Нужна помощь",
            callback_data=chose_role_callback.new(Roles.customer),
        ),
        InlineKeyboardButton(
            text="Стать помощником",
            callback_data=chose_role_callback.new(Roles.worker),
        ),
        InlineKeyboardButton(
            text="Пригласить",
            callback_data=chose_role_callback.new("invite"),
        )
    )
    return markup



