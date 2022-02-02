from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

get_location_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отправить локацию 📍",
                           request_location=True)
        ],
    ],
    resize_keyboard=True
)



