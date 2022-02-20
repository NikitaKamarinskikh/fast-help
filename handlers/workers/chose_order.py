from keyboards.inline.orders_nerby import orders_nearby_callback, chose_order_pagination_callback
from loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.orders_nerby import chose_order_markup, chose_order_callback, back_to_orders_callback
from states.workers.chose_order import ChoseOrderStates
from models import OrdersModel


def get_orders_by_category_name(orders: list, category_name: str, max_distance: int = 500):
    candidates = list()
    for order in orders:
        if order.category.name == category_name and order.distance <= max_distance:
            candidates.append(order)
    return candidates


async def get_message_content(order: object, orders_quantity: int, order_number: int):
    text = f"Заказ {order_number + 1} из {orders_quantity}\n{order.customer_name} {order.customer_phone}\n"
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
    category_id = callback_data.get("category_id")
    category_name = callback_data.get("category_name")
    orders = get_orders_by_category_name(orders, category_name)
    await state.update_data(category_orders=orders)
    await state.update_data(voice_messages_ids=[])
    await callback.message.answer(
        **(await get_message_content(orders[0], len(orders), 0))
    )
    if orders[0].voice_description:
        voice_message = await callback.message.answer_voice(
            orders[0].voice_description,
            caption="Описание задачи"
        )
        await state.update_data(voice_messages_ids=[voice_message.message_id])


@dp.callback_query_handler(chose_order_pagination_callback.filter(), state=ChoseOrderStates.chose_order)
async def flip_candidate(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    voice_messages_ids = state_data.get("voice_messages_ids")
    for message_id in voice_messages_ids:
        await bot.delete_message(chat_id=callback.from_user.id, message_id=message_id)
    await state.update_data(voice_messages_ids=[])
    order_number = int(callback_data.get("order_number"))
    orders = state_data.get("category_orders")
    order = orders[int(order_number)]
    await callback.message.edit_text(
        **(await get_message_content(order, len(orders), order_number))
    )
    if orders[int(order_number)].voice_description:
        voice_message = await callback.message.answer_voice(
            orders[int(order_number)].voice_description,
            caption="Описание задачи"
        )
        await state.update_data(voice_messages_ids=[voice_message.message_id])




