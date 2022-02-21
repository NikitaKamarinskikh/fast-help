from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.main import main_markup
from keyboards.inline.categories import create_categories_markup, get_category_callback
from keyboards.inline.start_or_back import start_or_back_markup
from keyboards.inline.yes_or_no import yes_or_no_markup, yes_or_no_callback
from loader import dp
from data.config import MainMenuCommands, Roles
from models import CustomersModel, JobCategoriesModel
from states.common.confirm_privacy_policy import ConfirmPrivacyPolicy
from states.customers.create_order import CreateOrderStates


@dp.message_handler(text=MainMenuCommands.workers_nearby)
async def workers_nearby(message: types.Message):
    try:
        customer = await CustomersModel.get_by_telegram_id(message.from_user.id)
        categories: list = await JobCategoriesModel.get_all()
        await message.answer(
            text="Выберите категорию",
            reply_markup=create_categories_markup(categories)
        )
        await CreateOrderStates.get_possible_category.set()
    except:
        await message.answer(
            text="Для того чтобы получить помощь понадобится заполнить небольшую анкету и согласиться с хранением "
                 "и обработкой данных и подписать договор оферту",
            reply_markup=start_or_back_markup(Roles.customer)
        )
        await ConfirmPrivacyPolicy.ask_to_confirm.set()


@dp.callback_query_handler(get_category_callback.filter(), state=CreateOrderStates.get_possible_category)
async def ask_to_confirm_possible_category(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    category_id: str = callback_data.get("category_id")
    await state.update_data(category_id=category_id)
    await callback.message.answer(
        text="Разместить задание в этой категории?",
        reply_markup=yes_or_no_markup(question="confirm_possible_category")
    )


@dp.callback_query_handler(yes_or_no_callback.filter(question="confirm_possible_category"),
                           state=CreateOrderStates.get_possible_category)
async def confirm_possible_category(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    choice = callback_data.get("choice")
    if choice == "yes":
        await callback.message.answer(
            text="Как к вам должны обращаться исполнители? ( Введите имя или имя отчество)",
            reply_markup=types.ReplyKeyboardRemove()
        )
        await CreateOrderStates.get_name.set()
    else:
        await state.finish()
        await callback.message.answer(
            text="Главное меню",
            reply_markup=main_markup
        )






