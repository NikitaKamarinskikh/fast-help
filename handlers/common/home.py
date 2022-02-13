from aiogram import types
from loader import dp
from keyboards.default.main import main_markup
from data.config import MainMenuCommands
from models import BotUsersModel


@dp.message_handler(text="Главное меню")
async def balance(message: types.Message):
    await message.answer(
        text="Гланое меню",
        reply_markup=main_markup
    )

