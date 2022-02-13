from aiogram import types
from loader import dp
from keyboards.inline.balance import balance_callback
from keyboards.inline.referral import referral_markup, referral_callback
from data.config import MainMenuCommands
from models import BotUsersModel


@dp.callback_query_handler(balance_callback.filter(option="invite"))
async def balance(callback: types.CallbackQuery):
    await callback.answer()
    bot_user = await BotUsersModel.get_by_telegram_id(callback.from_user.id)
    referrals = await BotUsersModel.get_referrals(bot_user)
    referrals_quantity = len(referrals)
    await callback.message.edit_text(
        text="Реферальная программа. \n"
             "За каждого приглашенного пользователя вы получаете (20) монет.\n"
             "Со всех внесенных пользователем платежей вы получаете (5)%.\n"
             f"Количество ваших рефералов: {referrals_quantity}",
        reply_markup=referral_markup()
    )


@dp.callback_query_handler(referral_callback.filter(option="get_link"))
async def get_referral_link(callback: types.CallbackQuery):
    await callback.answer()
    bot_name = (await callback.message.bot.get_me()).username
    link = f"https://t.me/{bot_name}?start={callback.from_user.id}"
    await callback.message.answer(f"Ваша реферальная ссылка:\n{link}")



