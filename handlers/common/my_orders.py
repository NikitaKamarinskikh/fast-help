from aiogram import types
from keyboards.inline.customer_orders import orders_markup, orders_callback, orders_status_callback, \
    orders_status_markup
from loader import dp
from keyboards.inline.start_or_back import start_or_back_markup, start_or_back_callback
from keyboards.inline.candidates_data import candidates_markup, candidate_callback
from data.config import Roles, MainMenuCommands, OrderStatuses
from states.common.confirm_privacy_policy import ConfirmPrivacyPolicy
from models import CustomersModel, OrdersModel, OrderCandidatesModel, WorkersModel
from handlers.customers.utils import get_orders_quantity_by_order_status


@dp.message_handler(text=MainMenuCommands.my_orders)
async def chose_orders_status(message: types.Message):
    try:
        customer = await CustomersModel.get_by_telegram_id(message.from_user.id)
        orders = await OrdersModel.get_not_completed(customer)
        in_progress_orders_quantity = get_orders_quantity_by_order_status(orders, OrderStatuses.in_progress)
        waiting_for_start_orders_quantity = get_orders_quantity_by_order_status(orders, OrderStatuses.waiting_for_start)

        worker = await WorkersModel.get_by_telegram_id(message.from_user.id)
        worker_orders = await OrdersModel.get_by_filters(worker=worker, status=OrderStatuses.in_progress)

        await message.answer(
            text="Ваши задания, в которых осуществляется подбор исполнителей, и там где они найдены.",
            reply_markup=orders_status_markup(waiting_for_start_orders_quantity, in_progress_orders_quantity,
                                              len(worker_orders))
        )
    except Exception as e:
        print(e)
        await message.answer(
            text="Для того чтобы получить помощь понадобится заполнить небольшую анкету и согласиться с хранением "
                 "и обработкой данных и подписать договор оферту",
            reply_markup=start_or_back_markup(Roles.customer)
        )
        await ConfirmPrivacyPolicy.ask_to_confirm.set()


@dp.callback_query_handler(orders_status_callback.filter(status=OrderStatuses.waiting_for_start))
async def show_waiting_for_start_orders(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    customer = await CustomersModel.get_by_telegram_id(callback.from_user.id)
    orders = await OrdersModel.get_by_filters(customer=customer, status=OrderStatuses.waiting_for_start)
    if len(orders):
        await callback.message.answer(
            text="Ваши задания",
            reply_markup=orders_markup(orders, OrderStatuses.waiting_for_start)
        )
    else:
        await callback.message.answer(
            text="Задания отсутствуют"
        )










