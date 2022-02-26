import time
from datetime import datetime, time
from aiogram import types
from aiogram.dispatcher import FSMContext
from handlers.customers.chose_candidate import get_order_finish_time_in_seconds
from common import parse_date, get_candidates_by_filters, correct_time
from keyboards.default.main import main_markup
from loader import dp
from keyboards.inline.update_order import update_order_start_date_callback, update_order_execution_time_markup, \
    update_order_execution_time_callback
from notifications import notify_workers_about_new_order
from states.customers.update_order import UpdateOrderStates
from data.config import OrderStatuses
from models import OrdersModel, OrderTimestampsModel


@dp.message_handler(state=UpdateOrderStates.get_start_date)
async def get_order_start_date(message: types.Message, state: FSMContext):
    date_time_str: str = message.text
    order_start_date_time = parse_date(date_time_str)
    if order_start_date_time is not None:
        await state.update_data(order_start_date_time=order_start_date_time.strftime("%Y-%m-%d %H:%M"))
        await message.answer(
            text="Время на выполнение задания (выберите кнопкой или введите самостоятельно текстом)",
            reply_markup=update_order_execution_time_markup()
        )
        await UpdateOrderStates.get_execution_time.set()
    else:
        await message.answer(
            text="Указан неверный формат, либо некоторые значения выходят за границы допустимого. Попробуйте еще раз"
        )


@dp.callback_query_handler(update_order_start_date_callback.filter(), state=UpdateOrderStates.get_start_date)
async def get_new_start_date_callback(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    await state.update_data(order_start_date_time=datetime.now().strftime("%Y-%m-%d %H:%M"))
    await callback.message.answer(
        text="Время на выполнение задания (выберите кнопкой или введите самостоятельно текстом "
             "в формате чч:мм (например 2:05))",
        reply_markup=update_order_execution_time_markup()
    )
    await UpdateOrderStates.get_execution_time.set()


async def update_order(state_data: dict):
    order_id = state_data.get("order_id")
    order = await OrdersModel.get_by_id(order_id)
    execution_time_str = state_data.get("order_execution_time")
    hours, minutes = execution_time_str.split(":")
    execution_time = time(int(hours), int(minutes), 0)
    update_data = {
        "start_date": state_data.get("order_start_date_time"),
        "execution_time": execution_time,
        "status": OrderStatuses.waiting_for_start
    }
    if not state_data.get("update_time_only"):
        await OrdersModel.update(order_id, **update_data)
        candidates = await get_candidates_by_filters(order, [])
        await notify_workers_about_new_order(candidates, order)
    else:
        timestamp_seconds = get_order_finish_time_in_seconds(execution_time)
        await OrdersModel.update(order_id, execution_time=execution_time)
        order = await OrdersModel.get_by_id(order_id)
        await OrderTimestampsModel.set_timestamp(order, timestamp_seconds)


@dp.callback_query_handler(update_order_execution_time_callback.filter(), state=UpdateOrderStates.get_execution_time)
async def update_order_execution_time_callback(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    execution_time = callback_data.get("time")
    await state.update_data(order_execution_time=execution_time.replace("-", ":"))
    state_data = await state.get_data()
    try:
        await update_order(state_data)
        if state_data.get("update_time_only"):
            await callback.message.answer(
                text="Время заказа успешно изменено"
            )
        else:
            await callback.message.answer(
                text="Заказ успешно обновлен и отправлен исполнителям рядом",
                reply_markup=main_markup
            )
        await state.finish()
    except Exception as e:
        print(e)
        await callback.message.answer(
            text="При изменении заказа возникла непредвиденная ошибка",
            reply_markup=main_markup
        )
        await state.finish()


@dp.message_handler(state=UpdateOrderStates.get_execution_time)
async def update_order_execution_time(message: types.Message, state: FSMContext):
    order_execution_time: str = message.text
    if correct_time(order_execution_time):
        await state.update_data(order_execution_time=order_execution_time)
        state_data = await state.get_data()
        try:
            await update_order(state_data)
            if state_data.get("update_time_only"):
                await message.answer(
                    text="Время заказа успешно изменено"
                )
            else:
                await message.answer(
                    text="Заказ успешно обновлен и отправлен исполнителям рядом",
                    reply_markup=main_markup
                )
            await state.finish()
        except Exception as e:
            print(e)
            await message.answer(
                text="При изменении заказа возникла непредвиденная ошибка",
                reply_markup=main_markup
            )
            await state.finish()
    else:
        await message.answer(
            text="Время указано в неправильном формате, либо выходит за границы допустимого. Попробуйте еще раз"
        )



