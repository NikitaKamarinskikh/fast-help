from aiogram import types
from keyboards.inline.customer_orders import orders_markup, orders_callback
from loader import dp
from keyboards.inline.complete_order import is_order_competed_callback, order_complete_denied_markup, \
    order_complete_denied_callback
from keyboards.inline.rating import rating_markup
from models import OrdersModel
from data.config import OrderStatuses
from notifications import notify_worker_about_completed_order


@dp.callback_query_handler(is_order_competed_callback.filter(choice="yes"))
async def confirm_order_complete(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    order_id = callback_data.get("order_id")
    await OrdersModel.update(int(order_id), status=OrderStatuses.completed)
    order = await OrdersModel.get_by_id(order_id)
    await callback.message.answer(
        text="Оцените исполнителя",
        reply_markup=rating_markup("customer", order.worker.pk, order.pk)
    )
    await notify_worker_about_completed_order(order)


@dp.callback_query_handler(is_order_competed_callback.filter(choice="no"))
async def deny_order_complete(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    order_id = int(callback_data.get("order_id"))
    order = await OrdersModel.get_by_id(order_id)
    await callback.message.answer(
        text="Что делаем?",
        reply_markup=order_complete_denied_markup(order_id, order.worker.pk)
    )


@dp.callback_query_handler(order_complete_denied_callback.filter(action="add_time"))
async def add_time_to_order_execution(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    await callback.message.answer("Тут будет вывод клавиатуры с выбором времени")


@dp.callback_query_handler(order_complete_denied_callback.filter(action="find_new_candidate"))
async def find_new_candidate(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    await callback.message.answer("Тут будет поиск нового кандидата")






