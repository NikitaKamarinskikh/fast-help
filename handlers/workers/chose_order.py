from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.orders_nerby import orders_nearby_callback, chose_order_pagination_callback
from loader import dp, bot
from keyboards.inline.orders_nerby import chose_order_markup, back_to_orders_callback
from states.workers.chose_order import ChoseOrderStates


async def get_message_content(order: object, orders_quantity: int, order_number: int):
    text = f"Задание {order_number + 1} из {orders_quantity}\n{order.customer_name} {order.customer_phone}\n"
    if order.customer.user.username and order.allow_to_write_in_telegram:
        text += f"@{order.customer.user.username}\n"
    else:
        text += "<b>Заказчик запретил писать ему в телеграмм</b>\n"
    text += f"Удаленность: {order.distance}м\n"
    if order.description:
        text += f"{order.description}\n"
    return {
        "text": text,
        "reply_markup": chose_order_markup(order_number, orders_quantity, order.pk)
    }

@dp.callback_query_handler(orders_nearby_callback.filter(), state=ChoseOrderStates.chose_order)
async def get_orders_nearby_by_category(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    orders = state_data.get("orders")
    category_name = callback_data.get("category_name")
    distance = int(callback_data.get("distance"))
    orders = _get_orders_by_category_name_and_max_distance(orders, category_name, distance)
    if len(orders):
        await state.update_data(category_orders=orders, voice_messages_ids=[])
        if orders[0].voice_description:
            await send_voice(callback, state, orders[0])
        await callback.message.answer(
            **(await get_message_content(orders[0], len(orders), 0))
        )
    else:
        await callback.message.answer("Задания отсутствуют")


@dp.callback_query_handler(chose_order_pagination_callback.filter(), state=ChoseOrderStates.chose_order)
async def move_candidate(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    voice_messages_ids = state_data.get("voice_messages_ids")
    for message_id in voice_messages_ids:
        await bot.delete_message(chat_id=callback.from_user.id, message_id=message_id)
    await state.update_data(voice_messages_ids=[])
    order_number = int(callback_data.get("order_number"))
    orders = state_data.get("category_orders")
    order = orders[int(order_number)]
    if orders[int(order_number)].voice_description:
        await send_voice(callback, state, orders[int(order_number)])
    await callback.message.answer(
        **(await get_message_content(order, len(orders), order_number))
    )
    await callback.message.delete()


async def send_voice(callback, state, order) -> None:
    voice_message = await callback.message.answer_voice(
        order.voice_description,
        caption="Описание задачи"
    )
    await state.update_data(voice_messages_ids=[voice_message.message_id])

def _get_orders_by_category_name_and_max_distance(orders: list, category_name: str, max_distance_in_meters: int = 500):
    candidates = list()
    for order in orders:
        if order.category_name == category_name and order.distance <= max_distance_in_meters:
            candidates.append(order)
    return candidates





