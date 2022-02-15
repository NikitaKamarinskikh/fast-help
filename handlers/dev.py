from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from models import BotUsersModel
from keyboards.default.start import start_keyboard
from keyboards.default.main import main_markup
from models import WorkersModel, BotUsersModel, OrdersModel

from notifications import notify_customer_about_completed_order


@dp.message_handler(commands=["dev"], state="*")
async def dev(message: types.Message, state: FSMContext):
    order = await OrdersModel.get_by_id(14)
    await notify_customer_about_completed_order(order)


# @dp.message_handler(state="*", content_types=types.ContentTypes.VOICE)
# async def dev1(message: types.Message, state: FSMContext):
#     voice_id = message.voice.file_id
#     print(voice_id)


