from aiogram.dispatcher import FSMContext

from data.config import OrderStatuses
from keyboards.inline.customer_orders import order_manage_callback, find_new_candidate_markup, \
    find_new_candidate_callback, orders_markup
from keyboards.inline.customer_orders import find_new_candidate_markup, find_new_candidate_callback
from keyboards.inline.rating import rating_markup, old_candidate_rating_markup, old_candidate_rating_callback
from keyboards.inline.update_order import update_order_start_date_markup
from loader import dp
from aiogram import types
from models import CustomersModel, OrdersModel, WorkersModel
from states.customers.update_order import UpdateOrderStates
from notifications import notify_worker_about_completed_order, notify_worker_about_new_feedback


@dp.callback_query_handler(order_manage_callback.filter(option="find_new_candidate"))
async def finish_order_execution(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    order_id = int(callback_data.get("order_id"))
    await callback.message.answer(
        text="Текущее задание отменится. Вы сможете оставить оценку исполнителю, а исполнитель вам. "
             "После этого вы сможете бесплатно подать точно такое же объявление с возможностью изменить "
             "дату начала и время на выполнение. Текст объявления, его место и контакты изменить нельзя.",
        reply_markup=find_new_candidate_markup(order_id)
    )


@dp.callback_query_handler(find_new_candidate_callback.filter(option="use_current"))
async def use_current_candidate(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    await callback.message.delete()
    customer = await CustomersModel.get_by_telegram_id(callback.from_user.id)
    orders = await OrdersModel.get_by_filters(customer=customer, status=OrderStatuses.in_progress)
    await callback.message.answer(
        text="Ваши задания",
        reply_markup=orders_markup(orders, OrderStatuses.in_progress)
    )


@dp.callback_query_handler(find_new_candidate_callback.filter(option="find_new"))
async def find_new_candidate(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    await callback.message.delete()
    order_id = int(callback_data.get("order_id"))
    order = await OrdersModel.get_by_id(order_id)
    await OrdersModel.update(order.pk, status=OrderStatuses.waiting_for_start)
    await notify_worker_about_completed_order(order)
    await OrdersModel.update(order_id, status=OrderStatuses.completed)
    await callback.message.answer(
        text="Оцените исполнителя",
        reply_markup=old_candidate_rating_markup(order.worker.pk, order.pk)
    )


@dp.callback_query_handler(old_candidate_rating_callback.filter())
async def old_candidate_rating(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer(cache_time=100)
    await callback.message.delete()
    order_id = int(callback_data.get("order_id"))
    value = int(callback_data.get("value"))
    worker_id = int(callback_data.get("worker_id"))
    order = await OrdersModel.get_by_id(order_id)
    worker = await WorkersModel.get_by_id(worker_id)
    current_completed_orders_quantity = worker.completed_orders_quantity
    current_rating = worker.rating + value
    new_completed_orders_quantity = current_completed_orders_quantity + 1
    await WorkersModel.update_worker_by_id(worker_id, completed_orders_quantity=new_completed_orders_quantity,
                                           rating=round(current_rating / new_completed_orders_quantity, 1))
    await notify_worker_about_new_feedback(order, value)
    await callback.message.answer("Исполнитель получил уведомление о вашй оценке")
    await callback.message.answer(
        text="Укажите дату и время начала задания.",
        reply_markup=update_order_start_date_markup()
    )
    await UpdateOrderStates.get_start_date.set()
    await state.update_data(order_id=order_id)







