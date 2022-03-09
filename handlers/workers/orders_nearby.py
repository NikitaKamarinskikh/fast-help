import logging
import time
from dataclasses import dataclass
from datetime import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from admin.workers.models import Workers
from data.config import MainMenuCommands, Roles, DAY_IN_SECONDS
from keyboards.inline.start_or_back import start_or_back_markup
from keyboards.inline.orders_nerby import orders_nearby_markup, orders_nearby_callback, \
    orders_at_longer_distance_markup, orders_at_longer_distance_callback, confirm_show_longer_distance_orders_markup, \
    confirm_show_longer_distance_orders_callback
from keyboards.default.home import main_meun_markup
from keyboards.inline.yes_or_no import yes_or_no_markup, yes_or_no_callback
from loader import dp
from models import WorkersModel, JobCategoriesModel, BotUsersModel
from states.common.confirm_privacy_policy import ConfirmPrivacyPolicy
from common import get_orders_by_worker
from states.workers.chose_order import ChoseOrderStates
from data.config import distances


@dataclass
class Categories:
    total_500_meters: int
    total_1000_meters: int
    total_1500_meters: int
    data_500: dict
    data_1000: dict
    data_1500: dict


def has_enough_coins(coins: int, distance: int) -> bool:
    if distance == distances.middle.meters:
        if coins >= distances.middle.worker_price:
            return True

    if distance == distances.long.meters:
        if coins >= distances.long.worker_price:
            return True
    return False


def has_access_to_orders_at_longer_distance_by_time(worker: object, distance: int) -> bool:
    if distance == distances.long.meters:
        if worker.max_distance == distances.long.meters:
            if worker.orders_at_longer_distance_access_time >= time.time():
                return True

    if distance == distances.middle.meters:
        if worker.max_distance >= distances.middle.meters:
            if worker.orders_at_longer_distance_access_time >= time.time():
                return True
    return False


def get_orders_at_longer_distance_access_time() -> int:
    return int(time.time()) + DAY_IN_SECONDS


def split_categories_by_orders(orders: list, worker_categories: list) -> Categories:
    """
    return: {"category_name": quantity}, {"category_name": quantity}
    """
    categories_data_500 = dict()
    categories_data_1000 = dict()
    categories_data_1500 = dict()
    for category in worker_categories:
        categories_data_500[category.name] = 0
        categories_data_1000[category.name] = 0
        categories_data_1500[category.name] = 0
    total_500_meters, total_1000_meters, total_1500_meters = 0, 0, 0

    for order in orders:
        order_category_name = order.category_name
        if order.distance <= 500:
            categories_data_500[order_category_name] += 1
            categories_data_1000[order_category_name] += 1
            categories_data_1500[order_category_name] += 1
            total_500_meters += 1
        elif order.distance <= 1000:
            categories_data_1500[order_category_name] += 1
            categories_data_1000[order_category_name] += 1
            total_1000_meters += 1
        elif order.distance <= 1500:
            categories_data_1500[order_category_name] += 1
            total_1500_meters += 1

    total_1000_meters += total_500_meters
    total_1500_meters += total_1000_meters
    return Categories(total_500_meters, total_1000_meters, total_1500_meters, categories_data_500,
                      categories_data_1000, categories_data_1500)


async def orders_exists(categories_data: Categories, distance: int):
    if distance == distances.middle.meters:
        if categories_data.total_1000_meters <= 0:
            return False
    if distance == distances.long.meters:
        if categories_data.total_1500_meters <= 0:
            return False
    return True


async def show_orders_at_longer_distance(callback: types.CallbackQuery, state: FSMContext, distance: int,
                                         remove_coins: bool = True):
    state_data = await state.get_data()
    categories = state_data.get("categories")
    if distance == distances.middle.meters:
        if remove_coins:
            await BotUsersModel.remove_coins(callback.from_user.id, distances.middle.worker_price)
        worker = await WorkersModel.get_by_telegram_id(callback.from_user.id)
        max_distance = distances.middle.meters
        if worker.max_distance == distances.long.meters:
            max_distance = distances.long.meters
        await WorkersModel.update_worker_by_id(
            worker.pk,
            orders_at_longer_distance_access_time=get_orders_at_longer_distance_access_time(),
            max_distance=max_distance
        )
        await callback.message.answer(
            text=f"Количество заданий в 1000м от вас: {categories.total_1000_meters}",
            reply_markup=orders_nearby_markup(categories.data_1000, distance)
        )
    elif distance == distances.long.meters:
        if remove_coins:
            await BotUsersModel.remove_coins(callback.from_user.id, distances.long.worker_price)
        worker = await WorkersModel.get_by_telegram_id(callback.from_user.id)
        await WorkersModel.update_worker_by_id(
            worker.pk,
            orders_at_longer_distance_access_time=get_orders_at_longer_distance_access_time(),
            max_distance=distances.long.meters
        )
        await callback.message.answer(
            text=f"Количество заданий в 1500м от вас: {categories.total_1500_meters}",
            reply_markup=orders_nearby_markup(categories.data_1500, distance)
        )


@dp.callback_query_handler(orders_at_longer_distance_callback.filter(), state=ChoseOrderStates.chose_order)
async def orders_at_longer_distance(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    distance = int(callback_data.get("distance"))
    user = await BotUsersModel.get_by_telegram_id(callback.from_user.id)
    worker = await WorkersModel.get_by_telegram_id(callback.from_user.id)
    categories_data = state_data.get("categories")

    if orders_exists(categories_data, distance):  # Если задания есть
        if not has_access_to_orders_at_longer_distance_by_time(worker, distance):  # Если нет доступа по времени
            if not has_enough_coins(user.coins, distance):  # Если недостаточно монет
                # Предложить пополнить баланс
                await callback.message.answer(
                    text="Недостаточно монет на счету. Хотите пополнить баланс?",
                    reply_markup=yes_or_no_markup("update_balance")
                )
            else:
                # Спросить уверен ли открыть задания
                await callback.message.answer(
                    text=f"Вы уверены, что хотите задания на {distance}м?",
                    reply_markup=confirm_show_longer_distance_orders_markup(distance)
                )
        else:
            # Открыть задания
            await show_orders_at_longer_distance(callback, state, distance, remove_coins=False)
    else:
        await callback.message.answer("Задания на данную дистанцию отсутствуют")


@dp.callback_query_handler(confirm_show_longer_distance_orders_callback.filter(choice="no"),
                           state=ChoseOrderStates.chose_order)
async def deny_showing_longer_distance_orders(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    categories = state_data.get("categories")
    await callback.message.answer(
        text=f"Количество заданий в 500м от вас: {categories.total_500_meters}",
        reply_markup=orders_nearby_markup(categories.data_500, distances.short.meters)
    )


# Задания на 1000 и 1500 метров
@dp.callback_query_handler(confirm_show_longer_distance_orders_callback.filter(choice="yes"),
                           state=ChoseOrderStates.chose_order)
async def show_longer_distance_orders(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    distance = int(callback_data.get("distance"))
    await show_orders_at_longer_distance(callback, state, distance)


@dp.message_handler(text=MainMenuCommands.tasks_nearby)
async def tasks_nearby(message: types.Message, state: FSMContext):
    try:
        worker = await WorkersModel.get_by_telegram_id(message.from_user.id)
        await message.answer("Ищу задания...", reply_markup=main_meun_markup)
        orders = await get_orders_by_worker(worker, max_distance=distances.long.meters)
        await state.update_data(categories=worker.categories.all())
        await state.update_data(orders=orders)

        categories = split_categories_by_orders(orders, worker.categories.all())

        await state.update_data(categories=categories)
        await message.answer(
            text=f"Количество заданий в 500м от вас: {categories.total_500_meters}",
            reply_markup=orders_nearby_markup(categories.data_500, distances.short.meters)
        )
        await message.answer(
            text=f"Можно открыть на 24 часа и откликнуться на задания в радиусе {distances.middle.meters}м "
                 f"и {distances.long.meters}м, "
                 f"за {distances.middle.worker_price} и {distances.long.worker_price} монет соотвественно.",
            reply_markup=orders_at_longer_distance_markup(categories.total_1000_meters, categories.total_1500_meters)
        )
        await ChoseOrderStates.chose_order.set()
    except Workers.DoesNotExist:
        await message.answer(
            text="Для того чтобы стать помощником понадобится заполнить небольшую анкету и "
                 "согласиться с хранением и обработкой данных",
            reply_markup=start_or_back_markup(Roles.worker)
        )
        await ConfirmPrivacyPolicy.ask_to_confirm.set()
    except Exception as e:
        logging.error(e)
        await message.answer(
            "Возникла непредвиденная ошибка. Повторите попытку позже"
        )








