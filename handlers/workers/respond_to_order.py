from aiogram import types
from loader import dp
from keyboards.inline.respond_to_order import respond_callback
from models import OrdersModel, WorkersModel
from notifications import notify_customer_about_new_response
from models import OrderCandidatesModel


@dp.callback_query_handler(respond_callback.filter())
async def respond_to_order(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    order_id = callback_data.get("order_id")
    worker = await WorkersModel.get_by_telegram_id(callback.from_user.id)
    try:
        order = await OrdersModel.get_available_by_id(int(order_id))
        await notify_customer_about_new_response(order, worker)
        await callback.message.answer(
            text="Заказчик получил уведомление, что вы готовы выполнить задание."
        )
        await OrderCandidatesModel.create(order, worker)
    except:
        await callback.message.answer("К сожалению, заказ был удален, либо передан другому исполнителю")


