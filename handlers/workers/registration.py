from aiogram.dispatcher import FSMContext
from aiogram import types
from loader import dp
from keyboards.inline.chose_role import chose_role_callback, chose_role_markup
from keyboards.inline.start_or_back import start_or_back_markup, start_or_back_callback
from keyboards.inline.agree_or_not import agree_or_not_markup, agree_or_not_callback
from keyboards.default.main import main_markup
from data.config import Roles
from data.config import InlineKeyboardAnswers
from models import BotUsersModel, WorkersModel
from states.common.confirm_privacy_policy import ConfirmPrivacyPolicy


@dp.callback_query_handler(chose_role_callback.filter(role=Roles.worker))
async def start_worker_registration(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        text="Для того чтобы стать помощником понадобится заполнить небольшую анкету и "
             "согласиться с хранением и обработкой данных",
        reply_markup=start_or_back_markup(Roles.worker)
    )
    await ConfirmPrivacyPolicy.ask_to_confirm.set()


@dp.callback_query_handler(start_or_back_callback.filter(choice=InlineKeyboardAnswers.get_back, role=Roles.worker),
                           state=ConfirmPrivacyPolicy.ask_to_confirm)
async def ask_to_confirm_privacy_policy(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.finish()
    await callback.message.answer(
        text="Добро пожаловать\nВы ищите помощь или хотите стать помощником?",
        reply_markup=chose_role_markup()
    )


@dp.callback_query_handler(start_or_back_callback.filter(choice=InlineKeyboardAnswers.start, role=Roles.worker),
                           state=ConfirmPrivacyPolicy.ask_to_confirm)
async def ask_to_confirm_privacy_policy(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(
        text="Прочитайте и подтвердите согласие",
        reply_markup=agree_or_not_markup(Roles.worker)
    )
    await ConfirmPrivacyPolicy.get_answer.set()


@dp.callback_query_handler(agree_or_not_callback.filter(choice=InlineKeyboardAnswers.agree, role=Roles.worker),
                           state=ConfirmPrivacyPolicy.get_answer)
async def confirm_privacy_policy(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    bot_user = await BotUsersModel.create_user(callback.from_user.id, callback.from_user.username)
    # worker = await WorkersModel.create_worker(bot_user)
    await callback.message.answer(
        text="Главное меню",
        reply_markup=main_markup
    )
    await state.finish()


@dp.callback_query_handler(agree_or_not_callback.filter(choice=InlineKeyboardAnswers.do_not_agree, role=Roles.worker),
                           state=ConfirmPrivacyPolicy.get_answer)
async def confirm_privacy_policy(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(
        text="Для того чтобы стать помощником понадобится заполнить небольшую анкету и "
             "согласиться с хранением и обработкой данных",
        reply_markup=start_or_back_markup(Roles.worker)
    )
    await ConfirmPrivacyPolicy.ask_to_confirm.set()

