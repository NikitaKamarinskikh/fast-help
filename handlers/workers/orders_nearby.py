import time
from dataclasses import dataclass
from datetime import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import MainMenuCommands, Roles
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


@dataclass
class Categories:
    total_500_meters: int
    total_1000_meters: int
    total_1500_meters: int
    data_500: dict
    data_1000: dict
    data_1500: dict


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
        # if order.distance <= 1500:
        #     categories_data_500[order.category.name] += 1
        #     categories_data_1000[order.category.name] += 1
        #     categories_data_1500[order.category.name] += 1
        #     total_1500_meters += 1
        # elif order.distance <= 1000:
        #     categories_data_500[order.category.name] += 1
        #     categories_data_1000[order.category.name] += 1
        #     total_1000_meters += 1
        # elif order.distance <= 500:
        #     categories_data_500[order.category.name] += 1
        #     total_500_meters += 1
        if order.distance <= 500:
            categories_data_500[order.category.name] += 1
            # categories_data_1000[order.category.name] += 1
            # categories_data_1500[order.category.name] += 1
            total_500_meters += 1
        elif order.distance <= 1000:
            # categories_data_500[order.category.name] += 1
            categories_data_1000[order.category.name] += 1
            total_1000_meters += 1
        elif order.distance <= 1500:
            # categories_data_500[order.category.name] += 1
            # categories_data_1000[order.category.name] += 1
            # categories_data_1000[order.category.name] += 1
            categories_data_1500[order.category.name] += 1
            total_1500_meters += 1
        # Количество

    return Categories(total_500_meters, total_1000_meters, total_1500_meters, categories_data_500,
                      categories_data_1000, categories_data_1500)


@dp.callback_query_handler(orders_at_longer_distance_callback.filter(), state=ChoseOrderStates.chose_order)
async def orders_at_longer_distance(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    distance = int(callback_data.get("distance"))
    user = await BotUsersModel.get_by_telegram_id(callback.from_user.id)
    worker = await WorkersModel.get_by_telegram_id(callback.from_user.id)
    if distance == 1000:
        if worker.max_distance < 1000:
            await callback.message.answer(
                text="Недостаточно монет на счету. Хотите пополнить баланс?",
                reply_markup=yes_or_no_markup("update_balance")
            )
            return
        if user.coins < 10:
            if time.time() > worker.orders_at_longer_distance_access_time:
                await callback.message.answer(
                        text="Недостаточно монет на счету. Хотите пополнить баланс?",
                        reply_markup=yes_or_no_markup("update_balance")
                    )
                return
    if distance == 1500:
        if worker.max_distance < 1500:
            await callback.message.answer(
                text="Недостаточно монет на счету. Хотите пополнить баланс?",
                reply_markup=yes_or_no_markup("update_balance")
            )
            return
        if user.coins < 20:
            if time.time() > worker.orders_at_longer_distance_access_time:
                await callback.message.answer(
                        text="Недостаточно монет на счету. Хотите пополнить баланс?",
                        reply_markup=yes_or_no_markup("update_balance")
                    )
                return

    await callback.message.answer(
        text=f"Вы уверены, что хотите задания на {distance}м?",
        reply_markup=confirm_show_longer_distance_orders_markup(distance)
    )


@dp.callback_query_handler(confirm_show_longer_distance_orders_callback.filter(choice="no"),
                           state=ChoseOrderStates.chose_order)
async def deny_showing_longer_distance_orders(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    orders = state_data.get("orders")
    categories = state_data.get("categories")
    categories = split_categories_by_orders(orders, categories)

    await callback.message.answer(
        text=f"Количество заданий в 500м от вас: {categories.total_500_meters}",
        reply_markup=orders_nearby_markup(categories.data_500, 500)
    )


# Задания на 1000 и 1500 метров
@dp.callback_query_handler(confirm_show_longer_distance_orders_callback.filter(choice="yes"),
                           state=ChoseOrderStates.chose_order)
async def show_longer_distance_orders(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    categories = state_data.get("categories")
    distance = int(callback_data.get("distance"))
    # user = await BotUsersModel.get_by_telegram_id(callback.from_user.id)
    # await callback.message.answer(f"coins: {user.coins}, distance: {distance}")
    if distance == 1000:
        await callback.message.answer(
            text=f"Количество заданий в 1000м от вас: {categories.total_1000_meters + categories.total_500_meters}",
            reply_markup=orders_nearby_markup(categories.data_1000, distance)
        )
    elif distance == 1500:
        await callback.message.answer(
            text=f"Количество заданий в 1000м от вас: {categories.total_1500_meters}",
            reply_markup=orders_nearby_markup(categories.data_1500, distance)
        )


@dp.message_handler(text=MainMenuCommands.tasks_nearby)
async def tasks_nearby(message: types.Message, state: FSMContext):
    try:
        worker = await WorkersModel.get_by_telegram_id(message.from_user.id)
        await message.answer("Ищу задания...", reply_markup=main_meun_markup)
        # categories = await JobCategoriesModel.get_all()
        orders = await get_orders_by_worker(worker, max_distance=1500)
        await state.update_data(categories=worker.categories.all())
        await state.update_data(orders=orders)

        print("start splitting categories", datetime.now().time())
        categories = split_categories_by_orders(orders, worker.categories.all())
        print("finish splitting categories", datetime.now().time())
        await state.update_data(categories=categories)
        await message.answer(
            text=f"Количество заданий в 500м от вас: {categories.total_500_meters}",
            reply_markup=orders_nearby_markup(categories.data_500, 500)
        )
        await message.answer(
            text="Можно открыть на (24) часа и откликнуться на задания в радиусе 1000м и 1500м, "
                 "за (10) и (20) монет соотвественно.",
            reply_markup=orders_at_longer_distance_markup(categories.total_1000_meters, categories.total_1500_meters)
        )
        await ChoseOrderStates.chose_order.set()
    except Exception as e:
        print(e, e.__class__)
        await message.answer(
            text="Для того чтобы стать помощником понадобится заполнить небольшую анкету и "
                 "согласиться с хранением и обработкой данных",
            reply_markup=start_or_back_markup(Roles.worker)
        )
        await ConfirmPrivacyPolicy.ask_to_confirm.set()









