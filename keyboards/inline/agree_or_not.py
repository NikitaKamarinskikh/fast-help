from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from data.config import InlineKeyboardAnswers

agree_or_not_callback = CallbackData("agree_or_not", "choice")


def agree_or_not_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text=InlineKeyboardAnswers.agree,
            callback_data=agree_or_not_callback.new(InlineKeyboardAnswers.agree),
        ),
        InlineKeyboardButton(
            text=InlineKeyboardAnswers.do_not_agree,
            callback_data=agree_or_not_callback.new(InlineKeyboardAnswers.do_not_agree),
        ),
    )
    return markup

