from aiogram import types
from keyboards.inline.customer_orders import orders_markup, orders_callback
from loader import dp
from keyboards.inline.complete_order import is_order_competed_callback
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



