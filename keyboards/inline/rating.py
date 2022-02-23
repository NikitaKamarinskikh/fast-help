from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

rating_callback = CallbackData("rating", "user_role", "user_id", "order_id", "value")
old_candidate_rating_callback = CallbackData("old_candidate_rating", "worker_id", "order_id", "value")


def rating_markup(user_role: str, user_id: int, order_id: int):
    markup = InlineKeyboardMarkup(row_width=5)
    for i in range(1, 6):
        markup.insert(
            InlineKeyboardButton(
                text=str(i),
                callback_data=rating_callback.new(user_role, user_id, order_id, i),
            ),
        )
    return markup


def old_candidate_rating_markup(worker_id: int, order_id: int):
    markup = InlineKeyboardMarkup(row_width=5)
    for i in range(1, 6):
        markup.insert(
            InlineKeyboardButton(
                text=str(i),
                callback_data=old_candidate_rating_callback.new(worker_id, order_id, i)
            ),
        )
    return markup


