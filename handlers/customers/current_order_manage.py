from aiogram import types
from keyboards.inline.rating import rating_markup
from loader import dp
from data.config import OrderStatuses
from keyboards.inline.customer_orders import orders_markup, orders_callback, orders_status_callback, \
    order_manage_markup, order_manage_callback, confirm_finish_order_markup, confirm_finish_order_callback
from models import OrdersModel, CustomersModel, OrderTimestampsModel
from notifications import notify_worker_about_completed_order


async def get_order_data(order_id: int):
    order = await OrdersModel.get_by_id(order_id)
    if order.description:
        text = f"Задание \"{order.description}\""
    else:
        text = f"Задание в категории \"{order.category.name}\""
    return {
        "text": text,
        "reply_markup": order_manage_markup(order_id)
    }


@dp.callback_query_handler(orders_status_callback.filter(status=OrderStatuses.in_progress))
async def show_in_progress_orders(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    customer = await CustomersModel.get_by_telegram_id(callback.from_user.id)
    orders = await OrdersModel.get_by_filters(customer=customer, status=OrderStatuses.in_progress)
    if len(orders):
        await callback.message.answer(
            text="Ваши задания",
            reply_markup=orders_markup(orders, OrderStatuses.in_progress)
        )
    else:
        await callback.message.answer(
            "Задания отсутствуют"
        )


@dp.callback_query_handler(orders_callback.filter(order_status=OrderStatuses.in_progress))
async def show_in_progress_order_data(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    order_id = int(callback_data.get("order_id"))
    await callback.message.answer(
        **(await get_order_data(order_id))
    )


@dp.callback_query_handler(order_manage_callback.filter(option="finish"))
async def finish_order_execution(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    order_id = int(callback_data.get("order_id"))
    await callback.message.edit_text(
        text="Вы уверены, что хотите завершить это задание?",
        reply_markup=confirm_finish_order_markup(order_id)
    )


@dp.callback_query_handler(confirm_finish_order_callback.filter())
async def confirm_finish_order(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer(cache_time=10)
    choice = callback_data.get("choice")
    order_id = int(callback_data.get("order_id"))
    order = await OrdersModel.get_by_id(order_id)
    if choice == "yes":
        await callback.message.delete()
        await notify_worker_about_completed_order(order)
        await OrdersModel.update(order_id, status=OrderStatuses.completed)
        await OrderTimestampsModel.delete_by_order(order)
        await callback.message.answer(
            text="Оцените исполнителя",
            reply_markup=rating_markup("customer", order.worker.pk, order.pk)
        )
    else:
        await callback.message.edit_text(
            **(await get_order_data(order_id))
        )







