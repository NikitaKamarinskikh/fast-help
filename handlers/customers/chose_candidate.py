from aiogram import types
from keyboards.inline.customer_orders import orders_markup, orders_callback
from loader import dp
from keyboards.inline.start_or_back import start_or_back_markup, start_or_back_callback
from keyboards.inline.candidates_data import candidates_markup, candidate_callback
from keyboards.inline.yes_or_no import yes_or_no_markup, yes_or_no_callback
from keyboards.inline.confirm_candidate import confirm_candidate_markup, confirm_candidate_callback
from data.config import Roles, MainMenuCommands
from states.common.confirm_privacy_policy import ConfirmPrivacyPolicy
from models import CustomersModel, OrdersModel, OrderCandidatesModel, WorkersModel
from notifications import notify_worker_about_being_chosen_as_implementer


@dp.callback_query_handler(orders_callback.filter())
async def show_order_candidates(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    order_id = int(callback_data.get("order_id"))
    order = await OrdersModel.get_by_id(order_id)
    candidates = await OrderCandidatesModel.get_by_order(order)
    if order.description:
        text = f"Исполнители на задание \"{order.description}\". Указан средний балл и количество выполненных заданий"
    else:
        text = f"Исполнители на задание в категории \"{order.category.name}\". Указан средний балл и количество " \
               f"выполненных заданий"

    await callback.message.answer(
        text=text,
        reply_markup=candidates_markup(candidates, order_id)
    )


@dp.callback_query_handler(candidate_callback.filter())
async def chose_candidate(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    worker_id = int(callback_data.get("candidate_id"))
    order_id = int(callback_data.get("order_id"))
    worker = await WorkersModel.get_by_id(worker_id)
    text = f"Выбрать {worker.name} исполнителем?"
    await callback.message.answer(
        text=text,
        reply_markup=confirm_candidate_markup(worker.pk, order_id)
    )


@dp.callback_query_handler(confirm_candidate_callback.filter())
async def confirm_chosen_candidate(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    choice = callback_data.get("choice")
    if choice == "yes":
        worker_id = int(callback_data.get("candidate_id"))
        order_id = int(callback_data.get("order_id"))
        worker = await WorkersModel.get_by_id(worker_id)
        order = await OrdersModel.get_by_id(order_id)
        await OrdersModel.update(order_id, worker=worker)
        await notify_worker_about_being_chosen_as_implementer(worker, order)
        await callback.message.answer("Тут еще будет вывод информации о выбранном кандидате")
    else:
        ...


