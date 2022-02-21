from dataclasses import dataclass
from datetime import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import MainMenuCommands, Roles
from keyboards.inline.start_or_back import start_or_back_markup
from keyboards.inline.orders_nerby import orders_nearby_markup, orders_nearby_callback, \
    orders_at_longer_distance_markup, orders_at_longer_distance_callback
from keyboards.default.home import main_meun_markup
from keyboards.inline.yes_or_no import yes_or_no_markup, yes_or_no_callback
from loader import dp
from models import WorkersModel, JobCategoriesModel
from states.common.confirm_privacy_policy import ConfirmPrivacyPolicy
from common import get_orders_by_worker
from states.workers.chose_order import ChoseOrderStates


@dataclass
class Categories:
    total_500_meters: int
    total_1000_meters: int
    total_1500_meters: int
    data: dict


def split_categories_by_orders(orders: list, categories: list) -> Categories:
    """
    return: {"category_name": quantity}, {"category_name": quantity}
    """
    categories_data = dict()

    total_500_meters, total_1000_meters, total_1500_meters = 0, 0, 0
    for order in orders:
        if order.distance <= 500:
            total_500_meters += 1
        elif order.distance <= 1000:
            total_1000_meters += 1
        elif order.distance <= 1500:
            total_1500_meters += 1
        # Количество
        if order.category.name not in categories_data.keys():
            categories_data[order.category.name] = 1
        else:
            categories_data[order.category.name] += 1
    print(categories_data)
    return Categories(total_500_meters, total_1000_meters, total_1500_meters, categories_data)


@dp.callback_query_handler(orders_at_longer_distance_callback.filter(), state=ChoseOrderStates.chose_order)
async def orders_at_longer_distance(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    distance = int(callback_data.get("distance"))
    await callback.message.answer(
        text=f"Вы уверены, что хотите задания на {distance}м?",
        reply_markup=yes_or_no_markup(question="show_longer_distance_orders")
    )


@dp.callback_query_handler(yes_or_no_callback.filter(question="show_longer_distance_orders"),
                           state=ChoseOrderStates.chose_order)
async def show_longer_distance_orders(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()


@dp.message_handler(text=MainMenuCommands.tasks_nearby)
async def tasks_nearby(message: types.Message, state: FSMContext):
    try:

        worker = await WorkersModel.get_by_telegram_id(message.from_user.id)
        await message.answer("Ищу задания...", reply_markup=main_meun_markup)
        categories = await JobCategoriesModel.get_all()
        orders = await get_orders_by_worker(worker, max_distance=1500)
        # await message.answer(str(len(orders)))
        print("start_updating_state_data", datetime.now().time())
        await state.update_data(orders=orders)
        print("finish_updating_data", datetime.now().time())
        print()

        print("start splitting categories", datetime.now().time())
        categories = split_categories_by_orders(orders, categories)
        print("finish splitting categories", datetime.now().time())

        await message.answer(
            text=f"Количество заданий в 500м от вас: {categories.total_500_meters}",
            reply_markup=orders_nearby_markup(categories.data)
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









