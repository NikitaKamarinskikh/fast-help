from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from data.config import InlineKeyboardAnswers

candidate_callback = CallbackData("candidate_data", "candidate_id", "order_id")


def candidates_markup(candidates: list, order_id: int):
    markup = InlineKeyboardMarkup(row_width=1)
    for candidate in candidates:
        markup.add(
            InlineKeyboardButton(
                text=f"{candidate.worker.name}",
                callback_data=candidate_callback.new(candidate.worker.pk, order_id),
            ),
        )
    return markup

