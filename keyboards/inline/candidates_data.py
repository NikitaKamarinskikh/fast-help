from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

candidate_callback = CallbackData("candidate_data", "candidate_id", "order_id", "candidate_number")
candidate_pagination_callback = CallbackData("candidate_pagination", "candidate_id", "order_id", "candidate_number",
                                             "direction")
show_order_candidates_callback = CallbackData("show_order_candidates", "order_id")


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
            callback_data=candidate_callback.new(candidate.pk, order_id, candidate_number),
        )
    )
    return markup


def show_order_candidates_markup(order_id: int):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            text="Перейти к заданию",
            callback_data=show_order_candidates_callback.new(order_id),
        )
    )
    return markup



