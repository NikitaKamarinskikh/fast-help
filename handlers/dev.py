from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from models import BotUsersModel
from keyboards.default.start import start_keyboard
from keyboards.default.main import main_markup
from models import WorkersModel, BotUsersModel


@dp.message_handler(commands=["dev"], state="*")
async def dev(message: types.Message, state: FSMContext):
    # worker = await WorkersModel.get_by_telegram_id(message.from_user.id)
    bot_user = await BotUsersModel.get_by_telegram_id(message.from_user.id)
    print(bot_user.__dict__)


