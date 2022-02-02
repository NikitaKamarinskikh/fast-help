from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.config import MainMenuCommands

main_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(MainMenuCommands.need_help)],
        [KeyboardButton(MainMenuCommands.change_data)],
        [KeyboardButton(MainMenuCommands.tasks_nearby)],
        [KeyboardButton(MainMenuCommands.workers_nearby)],
        [KeyboardButton(MainMenuCommands.my_tasks)],
        [KeyboardButton(MainMenuCommands.balance)],
    ],
    resize_keyboard=True
)


