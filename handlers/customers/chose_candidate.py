from time import time
from aiogram import types
from keyboards.inline.customer_orders import orders_markup, orders_callback
from loader import dp
from keyboards.inline.candidates_data import candidates_markup, candidate_callback, candidate_pagination_callback
from keyboards.inline.confirm_candidate import confirm_candidate_markup, confirm_candidate_callback
from models import CustomersModel, OrdersModel, OrderCandidatesModel, WorkersModel, OrderTimestampsModel
from notifications import notify_worker_about_being_chosen_as_implementer
from data.config import OrderStatuses


async def get_message_content(order_id: int, candidate_number: int):
    order = await OrdersModel.get_by_id(order_id)
    candidates = order.candidates.all()
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


@dp.callback_query_handler(orders_callback.filter(order_status=OrderStatuses.waiting_for_start))
async def show_order_candidates(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    order_id = int(callback_data.get("order_id"))
    await callback.message.answer(
        **(await get_message_content(order_id, 0))
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


def get_order_finish_time_in_seconds(order_time: time) -> int:
    hours = int(order_time.strftime("%H")) * 60
    minutes = int(order_time.strftime("%M"))
    return int(time()) + (hours + minutes) * 60


@dp.callback_query_handler(confirm_candidate_callback.filter())
async def confirm_chosen_candidate(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    choice = callback_data.get("choice")
    order_id = int(callback_data.get("order_id"))
    if choice == "yes":
        worker_id = int(callback_data.get("candidate_id"))
        worker = await WorkersModel.get_by_id(worker_id)
        order = await OrdersModel.get_by_id(order_id)
        await OrdersModel.update(order_id, worker=worker, status=OrderStatuses.in_progress)
        await notify_worker_about_being_chosen_as_implementer(worker, order)
        timestamp_seconds = get_order_finish_time_in_seconds(order.execution_time)
        await OrderTimestampsModel.set_timestamp(order, timestamp_seconds)
        await callback.message.answer("Тут еще будет вывод информации о выбранном кандидате")
    else:
        candidate_number = int(callback_data.get("candidate_number"))
        await callback.message.edit_text(
            **(await get_message_content(order_id, candidate_number))
        )


