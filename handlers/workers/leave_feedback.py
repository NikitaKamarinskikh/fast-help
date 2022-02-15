from loader import dp
from aiogram import types
from keyboards.inline.rating import rating_callback
from models import CustomersModel, OrdersModel
from notifications import notify_customer_about_new_feedback


@dp.callback_query_handler(rating_callback.filter(user_role="worker"))
async def leave_feedback_by_worker(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    customer_id = callback_data.get("user_id")
    value = int(callback_data.get("value"))
    order_id = int(callback_data.get("order_id"))
    order = await OrdersModel.get_by_id(order_id)
    customer = await CustomersModel.get_by_id(customer_id)
    current_completed_orders_quantity = customer.completed_orders_quantity
    current_rating = customer.rating + value
    new_completed_orders_quantity = current_completed_orders_quantity + 1
    await CustomersModel.update_by_id(customer_id, completed_orders_quantity=new_completed_orders_quantity,
                                      rating=round(current_rating / new_completed_orders_quantity, 2))
    await notify_customer_about_new_feedback(order, value)
    await callback.message.answer("Заказчик получил уведомление")
