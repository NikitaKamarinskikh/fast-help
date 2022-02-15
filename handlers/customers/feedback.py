from loader import dp
from aiogram import types
from keyboards.inline.rating import rating_callback
from models import WorkersModel, OrdersModel
from notifications import notify_worker_about_new_feedback


@dp.callback_query_handler(rating_callback.filter(user_role="customer"))
async def leave_feedback_by_customer(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    worker_id = callback_data.get("user_id")
    value = int(callback_data.get("value"))
    order_id = int(callback_data.get("order_id"))
    order = await OrdersModel.get_by_id(order_id)
    worker = await WorkersModel.get_by_id(worker_id)
    current_completed_orders_quantity = worker.completed_orders_quantity
    current_rating = worker.rating + value
    new_completed_orders_quantity = current_completed_orders_quantity + 1
    await WorkersModel.update_worker_by_id(worker_id, completed_orders_quantity=new_completed_orders_quantity,
                                           rating=round(current_rating / new_completed_orders_quantity, 2))
    await notify_worker_about_new_feedback(order, value)
    await callback.message.answer("Исполнитель получил уведомление")


