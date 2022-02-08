from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Нужна помощь")],
        [KeyboardButton("Стать помощником")],
        [KeyboardButton("Пригласить")],
    ],
    resize_keyboard=True
)


