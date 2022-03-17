from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

get_category_callback = CallbackData('category', 'category_id')
confirm_callback = CallbackData("confirm", "choice")


def create_categories_markup(categories: list, confirm_button=False):
    markup = InlineKeyboardMarkup(row_width=2)
    for category in categories:
        markup.insert(
            InlineKeyboardButton(
                text=category.name,
                callback_data=get_category_callback.new(category.pk),
            )
        )
    if confirm_button:
        markup.add(
            InlineKeyboardButton(
                text="Подтвердить",
                callback_data=confirm_callback.new("yes"),
            )
        )
    return markup


