from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

skip_callback = CallbackData("skip", "question")


def skip_markup(question: str):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="Пропустить",
            callback_data=skip_callback.new(question),
        )
    )
    return markup
