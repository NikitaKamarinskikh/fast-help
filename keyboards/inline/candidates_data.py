from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from data.config import InlineKeyboardAnswers

candidate_callback = CallbackData("candidate_data", "candidate_id", "order_id")
candidate_pagination_callback = CallbackData("candidate_pagination", "candidate_id", "order_id", "candidate_number",
                                             "direction")


def get_pagination_buttons(candidates_quantity: int, current_candidates_number: int,
                           candidate_id: int, order_id: int):
    if current_candidates_number < candidates_quantity and current_candidates_number == 0:
        return InlineKeyboardButton(text=">>",
                                    callback_data=candidate_pagination_callback.new(candidate_id, order_id,
                                                                                    current_candidates_number + 1,
                                                                                    "right"))
    elif current_candidates_number == candidates_quantity - 1:
        return InlineKeyboardButton(text="<<",
                                    callback_data=candidate_pagination_callback.new(candidate_id, order_id,
                                                                                    current_candidates_number - 1,
                                                                                    "left"))
    else:
        return InlineKeyboardButton(text=">>",
                                    callback_data=candidate_pagination_callback.new(candidate_id, order_id,
                                                                                    current_candidates_number + 1,
                                                                                    "right")), \
               InlineKeyboardButton(text="<<",
                                    callback_data=candidate_pagination_callback.new(candidate_id, order_id,
                                                                                    current_candidates_number - 1,
                                                                                    "left"))


def candidates_markup(candidate: object, candidate_number: int, candidates_quantity: int, order_id: int):
    markup = InlineKeyboardMarkup(row_width=2)
    if candidates_quantity > 1:
        if candidate_number < candidates_quantity and candidate_number == 0:
            markup.add(InlineKeyboardButton(text=">>",
                                            callback_data=candidate_pagination_callback.new(candidate.pk, order_id,
                                                                                            candidate_number + 1,
                                                                                            "right")))
        elif candidate_number == candidates_quantity - 1:
            markup.add(InlineKeyboardButton(text="<<",
                                            callback_data=candidate_pagination_callback.new(candidate.pk, order_id,
                                                                                            candidate_number - 1,
                                                                                            "left")))
        else:
            markup.add(InlineKeyboardButton(text="<<",
                                            callback_data=candidate_pagination_callback.new(candidate.pk, order_id,
                                                                                            candidate_number - 1,
                                                                                            "left")),
                       InlineKeyboardButton(text=">>",
                                            callback_data=candidate_pagination_callback.new(candidate.pk, order_id,
                                                                                            candidate_number + 1,
                                                                                            "right")))

    markup.add(
        InlineKeyboardButton(
            text="Выбрать",
            callback_data=candidate_callback.new(candidate.pk, order_id),
        )
    )
    return markup
