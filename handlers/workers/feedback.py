from aiogram import types

from common.rating import count_rating
from loader import dp
from keyboards.inline.rating import rating_callback
from models import CustomersModel, OrdersModel
from notifications import notify_customer_about_new_feedback


@dp.callback_query_handler(rating_callback.filter(user_role="worker"), state="*")
async def leave_feedback_by_worker(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer(cache_time=100)
    await callback.message.delete()
    customer_id = callback_data.get("user_id")
    value = int(callback_data.get("value"))
    order_id = int(callback_data.get("order_id"))
    order = await OrdersModel.get_by_id(order_id)
    customer = await CustomersModel.get_by_id(customer_id)
    await CustomersModel.update_by_id(customer_id, completed_orders_quantity=customer.completed_orders_quantity + 1,
                                      rating=count_rating(customer.rating, customer.completed_orders_quantity,
                                                          value))
    await notify_customer_about_new_feedback(order, value)
    await callback.message.answer("Заказчик получил уведомление")
