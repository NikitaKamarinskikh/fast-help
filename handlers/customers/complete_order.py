from aiogram import types
from datetime import datetime
from aiogram.dispatcher import FSMContext
from keyboards.inline.customer_orders import orders_markup, orders_callback, find_new_candidate_markup
from keyboards.inline.update_order import update_order_execution_time_markup
from loader import dp
from keyboards.inline.complete_order import is_order_competed_callback, order_complete_denied_markup, \
    order_complete_denied_callback
from keyboards.inline.rating import rating_markup
from models import OrdersModel, OrderTimestampsModel
from data.config import OrderStatuses
from notifications import notify_worker_about_completed_order
from states.customers.update_order import UpdateOrderStates


@dp.callback_query_handler(is_order_competed_callback.filter(choice="yes"))
async def confirm_order_complete(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer(cache_time=10)
    await callback.message.delete()
    order_id = int(callback_data.get("order_id"))
    await OrdersModel.update(int(order_id), status=OrderStatuses.completed)
    order = await OrdersModel.get_by_id(order_id)
    await OrderTimestampsModel.delete_by_order(order)
    await callback.message.answer(
        text="Оцените исполнителя",
        reply_markup=rating_markup("customer", order.worker.pk, order.pk)
    )
    await notify_worker_about_completed_order(order)


@dp.callback_query_handler(is_order_competed_callback.filter(choice="no"))
async def deny_order_complete(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer(cache_time=10)
    order_id = int(callback_data.get("order_id"))
    order = await OrdersModel.get_by_id(order_id)
    await callback.message.delete()
    await callback.message.answer(
        text="Что делаем?",
        reply_markup=order_complete_denied_markup(order_id, order.worker.pk)
    )


@dp.callback_query_handler(order_complete_denied_callback.filter(action="add_time"))
async def add_time_to_order_execution(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    order_id = int(callback_data.get("order_id"))
    await state.update_data(order_start_date_time=datetime.now().strftime("%Y-%m-%d %H:%M"))
    await state.update_data(update_time_only=True)
    await state.update_data(order_id=order_id)
    await callback.message.answer(
        text="Время на выполнение задания (выберите кнопкой или введите самостоятельно текстом "
             "в формате чч:мм (например 2:05))",
        reply_markup=update_order_execution_time_markup(order_id)
    )
    await UpdateOrderStates.get_execution_time.set()


@dp.callback_query_handler(order_complete_denied_callback.filter(action="find_new_candidate"))
async def find_new_candidate(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    order_id = int(callback_data.get("order_id"))
    await callback.message.answer(
        text="Текущее задание отменится. Вы сможете оставить оценку исполнителю, а исполнитель вам. "
             "После этого вы сможете бесплатно подать точно такое же объявление с возможностью изменить "
             "дату начала и время на выполнение. Текст объявления, его место и контакты изменить нельзя.",
        reply_markup=find_new_candidate_markup(order_id)
    )







