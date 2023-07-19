from aiogram import types

from common import get_candidates_by_filters
from keyboards.default.main import main_markup
from loader import dp
from keyboards.inline.send_order_to_workers import send_order_to_workers_callback
from models import OrdersModel
from notifications import notify_workers_about_new_order


@dp.callback_query_handler(send_order_to_workers_callback.filter())
async def send_oder_order_to_workers(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer(cache_time=100)
    await callback.message.delete()
    order_id = int(callback_data.get("order_id"))
    order = await OrdersModel.get_by_id(order_id)
    await callback.message.answer("Ищу исполнителей...")
    candidates = await get_candidates_by_filters(order, callback.from_user.id)
    await notify_workers_about_new_order(candidates, order)
    await callback.message.answer(
        text="Ваше задание отправлено исполнителям рядом",
        reply_markup=main_markup
    )


