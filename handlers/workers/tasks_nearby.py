from aiogram import types

from data.config import MainMenuCommands, Roles
from keyboards.inline.start_or_back import start_or_back_markup
from loader import dp
from models import WorkersModel
from states.common.confirm_privacy_policy import ConfirmPrivacyPolicy


@dp.message_handler(text=MainMenuCommands.tasks_nearby)
async def tasks_nearby(message: types.Message):
    try:
        worker = await WorkersModel.get_by_telegram_id(message.from_user.id)
        await message.answer("Тут будет вывод заказов")
    except:
        await message.answer(
            text="Для того чтобы стать помощником понадобится заполнить небольшую анкету и "
                 "согласиться с хранением и обработкой данных",
            reply_markup=start_or_back_markup(Roles.worker)
        )
        await ConfirmPrivacyPolicy.ask_to_confirm.set()


