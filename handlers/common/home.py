from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from keyboards.default.main import main_markup


@dp.message_handler(text="Главное меню", state="*")
async def balance(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        text="Гланое меню",
        reply_markup=main_markup
    )

