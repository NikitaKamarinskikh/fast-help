from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import MainMenuCommands, Roles
from keyboards.inline.start_or_back import start_or_back_markup
from loader import dp
from models import WorkersModel
from states.common.confirm_privacy_policy import ConfirmPrivacyPolicy
from states.workers.registration import WorkerRegistrationStates


@dp.message_handler(text=MainMenuCommands.change_data)
async def change_data(message: types.Message, state: FSMContext):
    try:
        worker = await WorkersModel.get_by_telegram_id(message.from_user.id)
        await message.answer(
            text="Как к вам должны обращаться заказчики? (Введите имя или имя отчество)",
            reply_markup=types.ReplyKeyboardRemove()
        )
        await WorkerRegistrationStates.get_name.set()
        await state.update_data(update=True)
    except Exception as e:
        await message.answer(
            text="Для того чтобы стать помощником понадобится заполнить небольшую анкету и "
                 "согласиться с хранением и обработкой данных",
            reply_markup=start_or_back_markup(Roles.worker)
        )
        await ConfirmPrivacyPolicy.ask_to_confirm.set()




