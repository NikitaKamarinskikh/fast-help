from aiogram import types

from loader import dp
from keyboards.inline.balance import balance_callback
from keyboards.inline.referral import referral_markup, referral_callback
from data.config import REFERRER_COINS, PROMOTIONAL_VIDEO_ID
from models import BotUsersModel
from data.config import MainMenuCommands


@dp.message_handler(text=["Пригласить", MainMenuCommands.referral_program])
async def invite(message: types.Message):
    bot_user = await BotUsersModel.get_by_telegram_id(message.from_user.id)
    referrals = await BotUsersModel.get_referrals(bot_user)
    referrals_quantity = len(referrals)
    await message.answer(
        text="Реферальная программа. \n"
             f"За каждого приглашенного пользователя вы получаете {REFERRER_COINS} монет.\n"
             "Со всех внесенных пользователем платежей вы получаете 5%.\n"
             f"Количество ваших рефералов: {referrals_quantity}",
        reply_markup=referral_markup()
    )


@dp.callback_query_handler(balance_callback.filter(option="invite"))
async def balance(callback: types.CallbackQuery):
    await callback.answer()
    bot_user = await BotUsersModel.get_by_telegram_id(callback.from_user.id)
    referrals = await BotUsersModel.get_referrals(bot_user)
    referrals_quantity = len(referrals)
    await callback.message.edit_text(
        text="Реферальная программа. \n"
             f"За каждого приглашенного пользователя вы получаете {REFERRER_COINS} монет.\n"
             "Со всех внесенных пользователем платежей вы получаете 5%.\n"
             f"Количество ваших рефералов: {referrals_quantity}",
        reply_markup=referral_markup()
    )


@dp.callback_query_handler(referral_callback.filter(option="get_link"))
async def get_referral_link(callback: types.CallbackQuery):
    await callback.answer()
    bot_name = (await callback.message.bot.get_me()).username
    link = f"https://t.me/{bot_name}?start={callback.from_user.id}"
    await callback.message.answer("Просто скопируй сообщение ниже или перешли его тому с кем хочешь поделиться")
    await callback.message.answer(
        text="Привет. Я нашел классного бота, в котором можно заработать, выполняя несложные задания рядом с "
             "домом. Для регистрации перейди по моей ссылке ниже, и мы оба получим дополнительные бонусы для "
             f"получения и размещения заданий. {link}"
    )
    await callback.message.answer_video(PROMOTIONAL_VIDEO_ID)


