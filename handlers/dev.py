from datetime import time, datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import OrderStatuses
from handlers.workers.registration import get_category_by_id
from loader import dp
from models import BotUsersModel, JobCategoriesModel, CustomersModel
from keyboards.default.start import start_keyboard
from keyboards.default.main import main_markup
from models import *

from notifications import notify_customer_about_completed_order
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

balance_callback = CallbackData("balance", "option")


def dev_markup():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(
            text="Выбрать",
            callback_data=balance_callback.new("update_balance"),
        )
    )
    markup.row(
        InlineKeyboardButton(
            text="<<",
            callback_data=balance_callback.new("invite"),
        ),
        InlineKeyboardButton(
            text=">>",
            callback_data=balance_callback.new("invite"),
        ),
    )
    return markup


@dp.message_handler(commands=["dev"], state="*")
async def dev(message: types.Message, state: FSMContext):
    # order = await OrdersModel.get_by_id(161158)
    # print(order.execution_time)
    # hours = int(order.execution_time.strftime("%H")) * 60
    # minutes = int(order.execution_time.strftime("%M"))
    # execution_time_in_seconds = (hours + minutes) * 60
    # print(hours, minutes, execution_time_in_seconds)
    # await OrdersModel.delete_all()
    # return
    # await WorkersModel.delete_all()
    # await message.answer("start making workers")
    # user = await BotUsersModel.get_by_telegram_id(message.from_user.id)
    # worker_data = {
    #     "user": user,
    #     "name": "test_user",
    #     "location": "54.983218 82.805607",
    #     "phone": "79237343772"
    # }
    #
    # worker = await WorkersModel.create_worker(**worker_data)
    #
    # categories = list()
    # categories_list = await JobCategoriesModel.get_all()
    # for category_id in [1, 3, 4, 5, 6]:
    #     categories.append(get_category_by_id(categories_list, int(category_id)))
    # await WorkersModel.add_categories_to_worker(worker, categories)
    #
    # for i in range(100000):
    #     worker = await WorkersModel.create_worker(**worker_data)
    #     await WorkersModel.add_categories_to_worker(worker, categories)
    #
    # await message.answer("finish making workers")
    # state_data = await state.get_data()
    # print(state_data)



    execution_time = time(int(10), int(20), 0)
    customer = await CustomersModel.get_by_telegram_id(message.from_user.id)
    category = await JobCategoriesModel.get_by_id(1)
    category_name = category.name
    location = f"54.983357  82.805794"
    order_data = {
        "customer": customer,
        "category": category,
        "customer_name": "test",
        "location": location,
        "customer_phone": "79237343772",
        "start_date": datetime.now(),
        "execution_time": execution_time,
        "allow_to_write_in_telegram": False,
        "category_name": category_name,
        "status": OrderStatuses.waiting_for_start
    }

    await message.answer("start making orders")
    for i in range(1, 20000):
        await OrdersModel.create(**order_data)
    await message.answer("finish making orders")



    # order = await OrdersModel.get_by_id(14)
    # await message.answer(
    #     text="Кандидат 2/7\nИмя: Анна\nРейтинг: 4.8\nВыполненных заданий: 10",
    #     reply_markup=dev_markup()
    # )
    #

# @dp.message_handler(state="*", content_types=types.ContentTypes.VOICE)
# async def dev1(message: types.Message, state: FSMContext):
#     voice_id = message.voice.file_id
#     print(voice_id)


