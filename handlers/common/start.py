from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp
from keyboards.default.start import start_keyboard
from keyboards.default.main import main_markup
from models import BotUsersModel, WorkersModel, CustomersModel, AdvertisingCompaniesModel
from notifications.notifications import notify_referrer_about_new_referral
from data.config import REFERRER_COINS


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


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    customer = await CustomersModel.get_or_none(message.from_user.id)
    worker = await WorkersModel.get_or_none(message.from_user.id)
    if customer or worker:
        await message.answer(
            text="Вы уже использовали эту команду",
            reply_markup=main_markup
        )
    else:
        message_args = message.get_args()
        print(message_args)
        referrer = None
        company = None
        if message_args.isdigit():  # Приведен пользователем
            print("Приведен пользователем")
            referrer = await get_referrer_by_message_args(message.get_args(), message.from_user.id)
        else:  # Пришел по ссылке от компани
            company_number = message.get_args().split("_")[-1]
            company = await AdvertisingCompaniesModel.get_by_number_or_none(company_number)
            if company:
                referrals_quantity = company.referrals_quantity + 1
                await AdvertisingCompaniesModel.update(company_number, referrals_quantity=referrals_quantity)
        user = await BotUsersModel.create_user(message.from_user.id, message.from_user.username, referrer)
        if not user.already_existed and referrer:
            referrer = await BotUsersModel.add_coins(referrer.telegram_id, REFERRER_COINS)
            await notify_referrer_about_new_referral(referrer)

        await message.answer(
            text="Добро пожаловать\nВы ищите помощь или хотите стать помощником?",
            reply_markup=start_keyboard
        )
        if company is None and referrer:
            await BotUsersModel.add_coins(message.from_user.id, REFERRER_COINS)
            await message.answer(f"Вам зачислен бонус {REFERRER_COINS} монет!")



