from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from models import BotUsersModel
from keyboards.default.start import start_keyboard
from keyboards.default.main import main_markup


@dp.message_handler(commands=["cancel"], state="*")
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    try:
        user = await BotUsersModel.get_by_telegram_id(message.from_user.id)
        await message.answer(
            text="Действие отменено. Сейчас вы находитесь в главном меню",
            reply_markup=main_markup
        )
    except:
        await message.answer(
            text="Добро пожаловать\nВы ищите помощь или хотите стать помощником?",
            reply_markup=start_keyboard
        )




