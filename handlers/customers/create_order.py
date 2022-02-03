from datetime import datetime
from aiogram.dispatcher import FSMContext
from aiogram import types

from keyboards.default.main import main_markup
from loader import dp
from keyboards.inline.categories import create_categories_markup, get_category_callback
from keyboards.inline.yes_or_no import yes_or_no_markup, yes_or_no_callback
from keyboards.inline.skip import skip_markup, skip_callback
from keyboards.inline.now import now_markup, now_callback
from keyboards.inline.order_execution_time import order_execution_time_markup, order_execution_time_callback
from keyboards.default.get_location import get_location_markup
from keyboards.default.get_phone import get_phone_markup
from data.config import Roles
from states.customers.create_order import CreateOrderStates
from models import JobCategoriesModel, CustomersModel, OrdersModel
from data.config import MainMenuCommands

from django.utils import timezone


@dp.message_handler(text=MainMenuCommands.need_help)
async def start_making_order(message: types.Message):
    categories: list = await JobCategoriesModel.get_all()
    await message.answer(
        text="Выберите категорию в которой нужен помощник",
        reply_markup=create_categories_markup(categories)
    )
    await CreateOrderStates.get_category.set()


@dp.callback_query_handler(get_category_callback.filter(), state=CreateOrderStates.get_category)
async def get_category(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    category_id: str = callback_data.get("category_id")
    await state.update_data(category_id=category_id)
    await callback.message.answer(
        text="Как к вам должны обращаться исполнители? ( Введите имя или имя отчество)",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await CreateOrderStates.get_name.set()


@dp.message_handler(state=CreateOrderStates.get_name)
async def get_name(message: types.Message, state: FSMContext):
    name: str = message.text
    await state.update_data(customer_name=name)
    await message.answer(
        text="Отправьте вашу локацию ( регистрироваться лучше там где вы проводите большую часть дня, "
             "для того чтобы вам приходили уведомления о заданиях рядом)",
        reply_markup=get_location_markup
    )
    await CreateOrderStates.get_location.set()


@dp.message_handler(content_types=types.ContentTypes.LOCATION, state=CreateOrderStates.get_location)
async def get_location(message: types.Message, state: FSMContext):
    location = message.location  # {"latitude": 10.123123, "longitude": 23.44233}
    await state.update_data(location=location)
    await message.answer(
        text="Укажите телефон для исполнителей",
        reply_markup=get_phone_markup
    )
    await CreateOrderStates.get_phone.set()


@dp.message_handler(content_types=types.ContentTypes.CONTACT, state=CreateOrderStates.get_phone)
async def get_phone(message: types.Message, state: FSMContext):
    phone: str = message.contact.phone_number
    await state.update_data(phone=phone)
    await message.answer(
        text="Может ли исполнитель написать вам в телеграм?",
        reply_markup=yes_or_no_markup("can_write", text_no="Только звонок")
    )
    await CreateOrderStates.cat_write.set()


@dp.callback_query_handler(yes_or_no_callback.filter(question="can_write"), state=CreateOrderStates.cat_write)
async def can_write(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    choice = callback_data.get('choice')
    if choice == "yes":
        await state.update_data(can_write=True)
    else:
        await state.update_data(can_write=False)
    await callback.message.answer(
        text="Вы хотите указать дополнительные контакты? Если да - введите всю информацию в строке ввода. "
             "Если нет нажмите кнопку пропустить",
        reply_markup=skip_markup("has_additional_contacts")
    )
    await CreateOrderStates.get_additional_contacts.set()


@dp.callback_query_handler(skip_callback.filter(question="has_additional_contacts"),
                           state=CreateOrderStates.get_additional_contacts)
async def has_additional_contacts_skip(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    await state.update_data(additional_contacts=None)
    await callback.message.answer(
        text="Напишите описание задачи или опишите голосом",
        reply_markup=skip_markup("order_description")
    )
    await CreateOrderStates.get_order_description.set()


@dp.message_handler(state=CreateOrderStates.get_additional_contacts)
async def has_additional_contacts(message: types.Message, state: FSMContext):
    additional_contacts: str = message.text
    await message.answer(
        text="Напишите описание задачи или опишите голосом",
        reply_markup=skip_markup("order_description")
    )
    await CreateOrderStates.get_order_description.set()
    await state.update_data(additional_contacts=additional_contacts)


@dp.callback_query_handler(skip_callback.filter(question="order_description"),
                           state=CreateOrderStates.get_order_description)
async def has_additional_contacts_skip(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    await state.update_data(order_description=None)
    await callback.message.answer(
        text="Укажите дату и время начала задания.",
        reply_markup=now_markup("order_start_date")
    )
    await CreateOrderStates.get_order_start_date.set()


@dp.message_handler(state=CreateOrderStates.get_order_description)
async def get_task_description(message: types.Message, state: FSMContext):
    task_description: str = message.text
    await state.update_data(order_description=task_description)
    await message.answer(
        text="Укажите дату и время начала задания",
        reply_markup=now_markup("order_start_date")
    )
    await CreateOrderStates.get_order_start_date.set()


@dp.message_handler(state=CreateOrderStates.get_order_start_date)
async def get_order_start_date(message: types.Message, state: FSMContext):
    date: str = message.text  # needs to be format %d.%m.%Y
    await state.update_data(order_start_date=date)
    await message.answer(
        text="Время на выполнение задания ( выберите кнопкой или введите самостоятельно текстом)",
        reply_markup=order_execution_time_markup()
    )
    await CreateOrderStates.get_order_execution_time.set()


@dp.callback_query_handler(now_callback.filter(question="order_start_date"),
                           state=CreateOrderStates.get_order_start_date)
async def get_order_start_date_now(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(order_start_date=datetime.now().strftime("%d.%m.%Y"))
    await callback.message.answer(
        text="Время на выполнение задания (выберите кнопкой или введите самостоятельно текстом)",
        reply_markup=order_execution_time_markup()
    )
    await CreateOrderStates.get_order_execution_time.set()


async def create_order(customer_telegram_id: int, state: FSMContext) -> bool:
    """
    state_data: {'category_id': '3', 'customer_name': 'Мой господин',
    'location': <Location {"latitude": 54.9834, "longitude": 82.806047}>,
    'phone': '79237343772', 'can_write': False,
    'additional_contacts': 'Почта - test@gmail.com', 'order_description': None,
    'order_start_date': '03.02.2022', 'order_execution_time': '120'}
    """
    state_data = await state.get_data()
    customer = await CustomersModel.get_by_telegram_id(customer_telegram_id)
    category = await JobCategoriesModel.get_by_id(state_data.get("category_id"))
    location = f"{state_data.get('location').latitude} {state_data.get('location').longitude}"
    order_data = {
        "customer": customer,
        "category": category,
        "customer_name": state_data.get("customer_name"),
        "location": location,
        "customer_phone": state_data.get("phone"),
        "start_date": timezone.now(),
        "execution_time": datetime.now().time()
    }
    if state_data.get("can_write"):
        order_data["customer_username"] = state_data.get("customer_username")
    if state_data.get("additional_contacts"):
        order_data["additional_contacts"] = state_data.get("additional_contacts")
    if state_data.get("order_description"):
        order_data["description"] = state_data.get("order_description")

    try:
        await OrdersModel.create(**order_data)
        return True
    except Exception as e:
        print(e)
        return False


@dp.callback_query_handler(order_execution_time_callback.filter(), state=CreateOrderStates.get_order_execution_time)
async def get_order_execution_time_callback(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    await state.update_data(order_execution_time_in_minutes=callback_data.get("time_in_minutes"))
    await state.update_data(customer_username=callback.message.from_user.username)
    if await create_order(callback.from_user.id, state):
        await callback.message.answer(
            text="Заказ успешно создан",
            reply_markup=main_markup
        )
        await state.finish()
        return
    await callback.message.answer(
        text="При создании заказа возникла непредвиденная ошибка",
        reply_markup=main_markup
    )
    await state.finish()


@dp.message_handler(state=CreateOrderStates.get_order_execution_time)
async def get_order_execution_time(message: types.Message, state: FSMContext):
    order_execution_time: str = message.text
    await state.update_data(order_execution_time_in_minutes=order_execution_time)
    await state.update_data(customer_username=message.from_user.username)
    if await create_order(message.from_user.id, state):
        await message.answer(
            text="Заказ успешно создан",
            reply_markup=main_markup
        )
        await state.finish()
        return
    await message.answer(
        text="При создании заказа возникла непредвиденная ошибка",
        reply_markup=main_markup
    )
    await state.finish()











