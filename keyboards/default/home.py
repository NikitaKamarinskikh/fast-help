from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_meun_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Главное меню")
        ],
    ],
    resize_keyboard=True,
)

