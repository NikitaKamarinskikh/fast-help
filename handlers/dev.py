from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from models import BotUsersModel
from keyboards.default.start import start_keyboard
from keyboards.default.main import main_markup
from models import WorkersModel, BotUsersModel, OrdersModel

from notifications import notify_customer_about_completed_order
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

balance_callback = CallbackData("balance", "option")


def dev_markup():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(
            text="Выбрать",
            callback_data=balance_callback.new("update_balance"),
        )
    )
    markup.row(
        InlineKeyboardButton(
            text="<<",
            callback_data=balance_callback.new("invite"),
        ),
        InlineKeyboardButton(
            text=">>",
            callback_data=balance_callback.new("invite"),
        ),
    )
    return markup


@dp.message_handler(commands=["dev"], state="*")
async def dev(message: types.Message, state: FSMContext):
    order = await OrdersModel.get_by_id(14)
    await message.answer(
        text="Кандидат 2/7\nИмя: Анна\nРейтинг: 4.8\nВыполненных заданий: 10",
        reply_markup=dev_markup()
    )


# @dp.message_handler(state="*", content_types=types.ContentTypes.VOICE)
# async def dev1(message: types.Message, state: FSMContext):
#     voice_id = message.voice.file_id
#     print(voice_id)


