from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

get_category_callback = CallbackData('category', 'category_id')


def create_categories_markup(categories: list):
    markup = InlineKeyboardMarkup(row_width=2)
    for category in categories:
        markup.add(
            InlineKeyboardButton(
                text=category.name,
                callback_data=get_category_callback.new(category.pk),
            )
        )
    return markup


