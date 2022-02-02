from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

yes_or_no_callback = CallbackData("yes_or_no", "question", "choice")


def yes_or_no_markup(question: str, text_yes: str = "Да", text_no: str = "Нет"):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text=text_yes,
            callback_data=yes_or_no_callback.new(question, "yes"),
        ),
        InlineKeyboardButton(
            text=text_no,
            callback_data=yes_or_no_callback.new(question, "no"),
        ),
    )
    return markup

