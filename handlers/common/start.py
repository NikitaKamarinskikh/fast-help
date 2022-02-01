from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp
from keyboards.inline.chose_role import chose_role_markup


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(
        text="Добро пожаловать\nВы ищите помощь или хотите стать помощником?",
        reply_markup=chose_role_markup()
    )


