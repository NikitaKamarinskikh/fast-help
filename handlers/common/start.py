from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp
from keyboards.default.start import start_keyboard
from keyboards.default.main import main_markup
from models import BotUsersModel, WorkersModel, CustomersModel


async def get_referrer_by_message_args(message_args, user_telegram_id: int):
    referrer = None
    if message_args:
        try:
            referrer_telegram_id = int(message_args)
            if referrer_telegram_id != user_telegram_id:
                referrer = await BotUsersModel.get_by_telegram_id(referrer_telegram_id)
        except Exception as e:
            print(e)
    return referrer


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    customer = await CustomersModel.get_or_none(message.from_user.id)
    worker = await WorkersModel.get_or_none(message.from_user.id)
    if customer or worker:
        await message.answer(
            text="Вы уже использовали эту команду",
            reply_markup=main_markup
        )
    else:
        referrer = await get_referrer_by_message_args(message.get_args(), message.from_user.id)
        user = await BotUsersModel.create_user(message.from_user.id, message.from_user.username, referrer)
        await message.answer(
            text="Добро пожаловать\nВы ищите помощь или хотите стать помощником?",
            reply_markup=start_keyboard
        )


