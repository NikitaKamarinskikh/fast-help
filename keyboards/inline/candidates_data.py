from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from data.config import InlineKeyboardAnswers

candidate_callback = CallbackData("candidate_data", "candidate_id", "order_id")


def cut_worker_name(worker_name: str):
    if len(worker_name) >= 20:
        worker_name = f"{worker_name[:17]}...".replace(" ", "")
    return worker_name


def candidates_markup(candidates: list, order_id: int):
    markup = InlineKeyboardMarkup(row_width=1)
    for candidate in candidates:
        markup.add(
            InlineKeyboardButton(
                text=f"{cut_worker_name(candidate.worker.name)} "
                     f"{candidate.worker.rating}/{candidate.worker.completed_orders_quantity}",
                callback_data=candidate_callback.new(candidate.worker.pk, order_id),
            ),
        )
    return markup

