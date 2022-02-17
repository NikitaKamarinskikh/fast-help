from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

confirm_candidate_callback = CallbackData("confirm_candidate", "choice", "candidate_id", "order_id", "candidate_number")


def confirm_candidate_markup(candidate_id: int, order_id: int, candidate_number: int):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="Да",
            callback_data=confirm_candidate_callback.new("yes", candidate_id, order_id, candidate_number),
        ),
        InlineKeyboardButton(
            text="Нет",
            callback_data=confirm_candidate_callback.new("no", candidate_id, order_id, candidate_number),
        ),
    )
    return markup

