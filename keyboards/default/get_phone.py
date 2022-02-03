from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


get_phone_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отправить номер телефона 📞",
                           request_contact=True)
        ],
    ],
    resize_keyboard=True,
)

