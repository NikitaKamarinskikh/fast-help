from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import OrderStatuses
from keyboards.default.home import main_meun_markup
from keyboards.inline.customer_orders import orders_status_callback
from keyboards.inline.executable_orders import executable_orders_markup, executable_orders_pagination_callback
from loader import dp, bot
from states.workers.executable_orders import ExecutableOrdersStates
from models import WorkersModel, OrdersModel


async def get_executable_order_data(worker_order: object, orders_number: int, orders_quantity: int) -> dict:
    text = f"Задание [{orders_number + 1} из {orders_quantity}]\n"
    if worker_order.description:
        text += f"Задание \"{worker_order.description}\"\n"
    else:
        text += f"Задание в категории \"{worker_order.category_name}\"\n"
    text += f"Средний балл заказчика: {worker_order.customer.rating}/" \
            f"{worker_order.customer.completed_orders_quantity}\n"
    return {
        "text": text,
        "reply_markup": executable_orders_markup(worker_order.pk, orders_number, orders_quantity)
    }


@dp.callback_query_handler(orders_status_callback.filter(status="executable"))
async def show_in_progress_orders(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    await callback.message.answer(
        text="Ищу задания...",
        reply_markup=main_meun_markup
    )
    worker = await WorkersModel.get_by_telegram_id(callback.from_user.id)
    worker_orders = await OrdersModel.get_by_filters(worker=worker, status=OrderStatuses.in_progress)
    await ExecutableOrdersStates.get_ordeer.set()

    if len(worker_orders):
        await state.update_data(executable_orders=worker_orders, voice_messages_ids=[])
        if worker_orders[0].voice_description:
            await callback.message.answer_voice(
                worker_orders[0].voice_description
            )
        await callback.message.answer(
            **(await get_executable_order_data(worker_orders[0], 0, len(worker_orders)))
        )
    else:
        await callback.message.answer(
            "Задания отсутствуют"
        )


async def send_voice(callback, state, order):
    voice_message = await callback.message.answer_voice(
        order.voice_description,
        caption="Описание задачи"
    )
    await state.update_data(voice_messages_ids=[voice_message.message_id])


@dp.callback_query_handler(executable_orders_pagination_callback.filter(), state=ExecutableOrdersStates.get_ordeer)
async def move_orders_to(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    voice_messages_ids = state_data.get("voice_messages_ids")
    for message_id in voice_messages_ids:
        await bot.delete_message(chat_id=callback.from_user.id, message_id=message_id)
    await state.update_data(voice_messages_ids=[])
    order_number = int(callback_data.get("order_number"))
    orders = state_data.get("executable_orders")
    order = orders[int(order_number)]
    if orders[int(order_number)].voice_description:
        await send_voice(callback, state, orders[int(order_number)])
    await callback.message.answer(
        **(await get_executable_order_data(order, order_number, len(orders)))
    )
    await callback.message.delete()


