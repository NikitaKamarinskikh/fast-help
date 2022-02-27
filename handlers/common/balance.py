from aiogram import types
from loader import dp
from keyboards.inline.balance import balance_markup
from data.config import MainMenuCommands
from models import BotUsersModel


@dp.message_handler(text=MainMenuCommands.balance)
async def balance(message: types.Message):
    bot_user = await BotUsersModel.get_by_telegram_id(message.from_user.id)
    await message.answer(
        text=f"Баланс {bot_user.coins} монет\n"
             "Вы можете пополнить баланс внеся оплату или пригласив друзей.",
        reply_markup=balance_markup()
    )



