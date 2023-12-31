from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from data.config import InlineKeyboardAnswers

start_or_back_callback = CallbackData("start_or_back", "role", "choice")


def start_or_back_markup(role: str):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text=InlineKeyboardAnswers.start,
            callback_data=start_or_back_callback.new(role, InlineKeyboardAnswers.start),
        ),
        InlineKeyboardButton(
            text=InlineKeyboardAnswers.get_back,
            callback_data=start_or_back_callback.new(role, InlineKeyboardAnswers.get_back),
        ),
    )
    return markup


