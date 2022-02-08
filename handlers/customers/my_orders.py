from aiogram.dispatcher import FSMContext
from aiogram import types

from keyboards.inline.categories import create_categories_markup
from keyboards.inline.customer_orders import orders_markup
from loader import dp
from keyboards.inline.chose_role import chose_role_callback, chose_role_markup
from keyboards.inline.start_or_back import start_or_back_markup, start_or_back_callback
from keyboards.inline.agree_or_not import agree_or_not_markup, agree_or_not_callback
from keyboards.default.main import main_markup
from data.config import Roles, MainMenuCommands
from data.config import InlineKeyboardAnswers
from models import BotUsersModel, CustomersModel, JobCategoriesModel
from states.common.confirm_privacy_policy import ConfirmPrivacyPolicy
from states.customers.create_order import CreateOrderStates
from models import CustomersModel, OrdersModel


@dp.message_handler(text=MainMenuCommands.my_orders)
async def start_making_order(message: types.Message):
    try:
        customer = await CustomersModel.get_by_telegram_id(message.from_user.id)
        orders = await OrdersModel.get_by_filters(customer=customer)
        await message.answer(
            text="Ваши задания: (кнопки еще не работают)",
            reply_markup=orders_markup(orders)
        )
    except Exception as e:
        print(e)
        await message.answer(
            text="Для того чтобы получить помощь понадобится заполнить небольшую анкету и согласиться с хранением "
                 "и обработкой данных и подписать договор оферту",
            reply_markup=start_or_back_markup(Roles.customer)
        )
        await ConfirmPrivacyPolicy.ask_to_confirm.set()
