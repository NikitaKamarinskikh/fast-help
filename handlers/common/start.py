from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp
from keyboards.inline.chose_role import chose_role_markup
from keyboards.default.main import main_markup
from models import BotUsersModel


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        user = await BotUsersModel.get_by_telegram_id(message.from_user.id)
        await message.answer(
            text="Вы уже использовали эту команду",
            reply_markup=main_markup
        )
    except:
        await message.answer(
            text="Добро пожаловать\nВы ищите помощь или хотите стать помощником?",
            reply_markup=chose_role_markup()
        )


