from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

now_callback = CallbackData("now", "question")


def now_markup(question: str):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="Сейчас",
            callback_data=now_callback.new(question),
        )
    )
    return markup
