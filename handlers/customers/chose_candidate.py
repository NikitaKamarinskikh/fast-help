import time
from datetime import datetime
from aiogram import types
from keyboards.inline.customer_orders import orders_markup, orders_callback
from loader import dp
from keyboards.inline.candidates_data import candidates_markup, candidate_callback, candidate_pagination_callback, \
    show_order_candidates_callback
from keyboards.inline.confirm_candidate import confirm_candidate_markup, confirm_candidate_callback
from models import CustomersModel, OrdersModel, OrderCandidatesModel, WorkersModel, OrderTimestampsModel
from notifications import notify_worker_about_being_chosen_as_implementer
from data.config import OrderStatuses


async def get_message_content(order_id: int, candidate_number: int):
    order = await OrdersModel.get_by_id(order_id)
    candidates = order.candidates.all()
    if len(candidates):
        if order.description:
            text = f"Исполнители на задание \"{order.description}\". Указан средний балл и количество выполненных заданий\n"
        else:
            text = f"Исполнители на задание в категории \"{order.category.name}\". Указан средний балл и количество " \
                   f"выполненных заданий\n"

        text += f"{candidates[candidate_number].name} [{candidate_number + 1} из {len(candidates)}]\n" \
                f"Средний балл: {candidates[candidate_number].rating}\n" \
                f"Заданий выполнено: {candidates[candidate_number].completed_orders_quantity}"
        return {
            "text": text,
            "reply_markup": candidates_markup(candidates[candidate_number], candidate_number, len(candidates), order_id)
        }
    return {
        "text": "Откликов на это задание еще нет"
    }


@dp.callback_query_handler(orders_callback.filter(order_status=OrderStatuses.waiting_for_start))
async def show_order_candidates(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    order_id = int(callback_data.get("order_id"))
    order = await OrdersModel.get_by_id(order_id)
    if not order.worker:
        await callback.message.answer(
            **(await get_message_content(order_id, 0))
        )
    else:
        await callback.message.answer(
            text="Иполнитель уже выбран"
        )


@dp.callback_query_handler(show_order_candidates_callback.filter(), state="*")
async def show_order_candidates_by_callback(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    order_id = int(callback_data.get("order_id"))
    order = await OrdersModel.get_by_id(order_id)
    if not order.worker:
        await callback.message.answer(
            **(await get_message_content(order_id, 0))
        )
    else:
        await callback.message.answer(
            text="Иполнитель уже выбран"
        )


@dp.callback_query_handler(candidate_pagination_callback.filter())
async def flip_candidate(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    order_id = int(callback_data.get("order_id"))
    candidate_number = int(callback_data.get("candidate_number"))
    await callback.message.edit_text(
        **(await get_message_content(order_id, candidate_number))
    )


@dp.callback_query_handler(candidate_callback.filter())
async def chose_candidate(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    worker_id = int(callback_data.get("candidate_id"))
    order_id = int(callback_data.get("order_id"))
    candidate_number = int(callback_data.get("candidate_number"))
    worker = await WorkersModel.get_by_id(worker_id)
    text = f"Выбрать {worker.name} исполнителем?"
    await callback.message.edit_text(
        text=text,
        reply_markup=confirm_candidate_markup(worker.pk, order_id, candidate_number)
    )


def get_order_finish_time_in_seconds(order: object, from_now: bool = False, seconds: int = 0) -> int:
    hours = int(order.execution_time.strftime("%H")) * 60
    minutes = int(order.execution_time.strftime("%M"))
    state_date_in_seconds = time.mktime(order.start_date.timetuple()) - (60 * 60)
    if from_now:
        return int(datetime.today().timestamp()) + seconds
    elif datetime.now().timestamp() > order.start_date.timestamp() - (4 * 60 * 60):
        return int(datetime.now().timestamp()) + ((hours + minutes) * 60)
    return int(state_date_in_seconds + ((hours + minutes) * 60))


@dp.callback_query_handler(confirm_candidate_callback.filter())
async def confirm_chosen_candidate(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer(cache_time=10)
    choice = callback_data.get("choice")
    order_id = int(callback_data.get("order_id"))
    if choice == "yes":
        await callback.message.delete()
        worker_id = int(callback_data.get("candidate_id"))
        worker = await WorkersModel.get_by_id(worker_id)
        order = await OrdersModel.get_by_id(order_id)
        await OrdersModel.update(order_id, worker=worker, status=OrderStatuses.in_progress)
        await notify_worker_about_being_chosen_as_implementer(worker, order)
        timestamp_seconds = get_order_finish_time_in_seconds(order)
        await OrderTimestampsModel.set_timestamp(order, timestamp_seconds)
        worker_data = f"{worker.name} {worker.rating}/{worker.completed_orders_quantity}\n" \
                      f"Телефон: {worker.phone}\n"
        if worker.additional_contacts:
            worker_data += worker.additional_contacts
        await callback.message.answer(
            text=worker_data
        )
    else:
        candidate_number = int(callback_data.get("candidate_number"))
        await callback.message.edit_text(
            **(await get_message_content(order_id, candidate_number))
        )


