from datetime import datetime
from aiogram.dispatcher import FSMContext
from aiogram import types
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
from models import JobCategoriesModel
from data.config import MainMenuCommands


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
    await state.update_data(name=name)
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
        text="Укажите дату и время начала задания.",
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











