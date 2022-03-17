import logging

from aiogram.dispatcher import FSMContext
from aiogram import types
from admin.customers.models import Customers
from keyboards.default.start import start_keyboard
from keyboards.inline.categories import create_categories_markup
from loader import dp
from keyboards.inline.chose_role import chose_role_callback, chose_role_markup
from keyboards.inline.start_or_back import start_or_back_markup, start_or_back_callback
from keyboards.inline.agree_or_not import agree_or_not_markup, agree_or_not_callback
from keyboards.default.main import main_markup
from data.config import Roles, MainMenuCommands
from data.config import InlineKeyboardAnswers
from models import BotUsersModel, CustomersModel, JobCategoriesModel, DocumentsModel, WorkersModel
from states.common.confirm_privacy_policy import ConfirmPrivacyPolicy
from states.customers.create_order import CreateOrderStates


@dp.message_handler(text=MainMenuCommands.need_help)
async def start_making_order(message: types.Message):
    try:
        customer = await CustomersModel.get_by_telegram_id(message.from_user.id)
        if customer.is_privacy_policy_confirmed:
            categories: list = await JobCategoriesModel.get_all()
            await message.answer(
                text="Выберите категорию в которой нужен помощник",
                reply_markup=types.ReplyKeyboardRemove()
            )
            await message.answer(
                text="Категории",
                reply_markup=create_categories_markup(categories)
            )
            await CreateOrderStates.get_category.set()
        else:
            await message.answer(
                text="Для того чтобы получить помощь понадобится заполнить небольшую анкету и согласиться с хранением "
                     "и обработкой данных и подписать договор оферту",
                reply_markup=start_or_back_markup(Roles.customer)
            )
            await ConfirmPrivacyPolicy.ask_to_confirm.set()
    except Customers.DoesNotExist:
        await message.answer(
            text="Для того чтобы получить помощь понадобится заполнить небольшую анкету и согласиться с хранением "
                 "и обработкой данных и подписать договор оферту",
            reply_markup=start_or_back_markup(Roles.customer)
        )
        await ConfirmPrivacyPolicy.ask_to_confirm.set()
    except Exception as e:
        logging.exception(e)
        await message.answer("При обработке запроса возникла непредвиденная ошибка")


@dp.callback_query_handler(start_or_back_callback.filter(choice=InlineKeyboardAnswers.get_back, role=Roles.customer),
                           state=ConfirmPrivacyPolicy.ask_to_confirm)
async def ask_to_confirm_privacy_policy(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.finish()
    worker = await WorkersModel.get_or_none(callback.from_user.id)
    if worker:
        await callback.message.answer(
            text="Главное меню",
            reply_markup=main_markup
        )
    else:
        await callback.message.answer(
            text="Добро пожаловать\nВы ищите помощь или хотите стать помощником?",
            reply_markup=start_keyboard
        )


@dp.callback_query_handler(start_or_back_callback.filter(choice=InlineKeyboardAnswers.start, role=Roles.customer),
                           state=ConfirmPrivacyPolicy.ask_to_confirm)
async def ask_to_confirm_privacy_policy(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    documents = await DocumentsModel.get_by_user_category("customers")
    for document in documents:
        await callback.message.answer_document(document.telegram_id)
    await callback.message.answer(
        text="Прочитайте и подтвердите согласие",
        reply_markup=agree_or_not_markup(Roles.customer)
    )
    await ConfirmPrivacyPolicy.get_answer.set()


@dp.callback_query_handler(agree_or_not_callback.filter(choice=InlineKeyboardAnswers.agree, role=Roles.customer),
                           state=ConfirmPrivacyPolicy.get_answer)
async def confirm_privacy_policy(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    bot_user = await BotUsersModel.get_by_telegram_id(callback.from_user.id)
    await state.finish()
    try:
        customer = await CustomersModel.get_by_telegram_id(callback.from_user.id)
        await CustomersModel.update_by_id(customer.pk, is_privacy_policy_confirmed=True)
    except:
        customer = await CustomersModel.create_customer(bot_user)
    categories: list = await JobCategoriesModel.get_all()
    await callback.message.answer(
        text="Выберите категорию в которой нужен помощник",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await callback.message.answer(
        text="Категории",
        reply_markup=create_categories_markup(categories)
    )
    await CreateOrderStates.get_category.set()


@dp.callback_query_handler(agree_or_not_callback.filter(choice=InlineKeyboardAnswers.do_not_agree, role=Roles.customer),
                           state=ConfirmPrivacyPolicy.get_answer)
async def confirm_privacy_policy(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(
        text="Для того чтобы получить помощь понадобится заполнить небольшую анкету и согласиться с хранением "
             "и обработкой данных и подписать договор оферту",
        reply_markup=start_or_back_markup(Roles.customer)
    )
    await ConfirmPrivacyPolicy.ask_to_confirm.set()
