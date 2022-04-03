from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.config import MainMenuCommands

# main_markup = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(MainMenuCommands.need_help), KeyboardButton(MainMenuCommands.change_data)],
#         [KeyboardButton(MainMenuCommands.tasks_nearby), KeyboardButton(MainMenuCommands.my_orders)],
#         [KeyboardButton(MainMenuCommands.balance), KeyboardButton(MainMenuCommands.referral_program)],
#     ],
#     resize_keyboard=True
# )

main_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(MainMenuCommands.tasks_nearby), KeyboardButton(MainMenuCommands.my_orders)],
        [KeyboardButton(MainMenuCommands.balance), KeyboardButton(MainMenuCommands.referral_program)],
        [KeyboardButton(MainMenuCommands.change_data)]
    ],
    resize_keyboard=True
)


