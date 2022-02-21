from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from models import BotUsersModel, WorkersModel, CustomersModel
from keyboards.default.start import start_keyboard
from keyboards.default.main import main_markup


@dp.message_handler(commands=["cancel"], state="*")
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()

    customer = await CustomersModel.get_or_none(message.from_user.id)
    worker = await WorkersModel.get_or_none(message.from_user.id)
    if customer or worker:
        await message.answer(
            text="Действие отменено. Сейчас вы находитесь в главном меню",
            reply_markup=main_markup
        )
    else:
        await message.answer(
            text="Добро пожаловать\nВы ищите помощь или хотите стать помощником?",
            reply_markup=start_keyboard
        )




