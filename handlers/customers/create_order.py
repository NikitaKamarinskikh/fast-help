from datetime import datetime, time
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
from states.customers.create_order import CreateOrderStates
from models import JobCategoriesModel, CustomersModel, OrdersModel
from data.config import MainMenuCommands
from common import parse_date, correct_time, get_candidates_by_filters
from notifications import notify_workers_about_new_order


@dp.callback_query_handler(get_category_callback.filter(), state=CreateOrderStates.get_category)
async def get_category(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    await state.update_data(customer_username=callback.from_user.username)
    category_id: str = callback_data.get("category_id")
    await state.update_data(category_id=category_id)
    await callback.message.answer(
        text="Как к вам должны обращаться исполнители? (Введите имя или имя отчество)",
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
    if message.contact.user_id == message.from_user.id:
        phone: str = message.contact.phone_number
        await state.update_data(phone=phone)
        await message.answer(
            text="Телефон принят (это сообщение нужно, что бы удалить кнопку для отправки телефона)",
            reply_markup=types.ReplyKeyboardRemove()
        )
        await message.answer(
            text="Может ли исполнитель написать вам в телеграм?",
            reply_markup=yes_or_no_markup("can_write", text_no="Только звонок")
        )
        await CreateOrderStates.cat_write.set()
    else:
        await message.answer("Похоже, вы использовали чужой номер телефона. Воспользуйтесь кнопкой, чтобы отправить "
                             "свой номер телефона")


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


@dp.message_handler(state=CreateOrderStates.get_order_description, content_types=types.ContentTypes.VOICE)
async def get_description_by_voice(message: types.Message, state: FSMContext):
    voice_id = message.voice.file_id
    await state.update_data(order_voice_description=voice_id)
    await message.answer(
        text="Укажите дату и время начала задания. Необходимый формат: дд.мм.гггг чч:мм (например 07.11.2022 15:30 )",
        reply_markup=now_markup("order_start_date")
    )
    await CreateOrderStates.get_order_start_date.set()


@dp.callback_query_handler(skip_callback.filter(question="order_description"),
                           state=CreateOrderStates.get_order_description)
async def has_additional_contacts_skip(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    await state.update_data(order_description=None)
    await callback.message.answer(
        text="Укажите дату и время начала задания. Необходимый формат: дд.мм.гггг чч:мм (например 07.11.2022 15:30 )",
        reply_markup=now_markup("order_start_date")
    )
    await CreateOrderStates.get_order_start_date.set()


@dp.message_handler(state=CreateOrderStates.get_order_description)
async def get_task_description(message: types.Message, state: FSMContext):
    task_description: str = message.text
    await state.update_data(order_description=task_description)
    await message.answer(
        text="Укажите дату и время начала задания. Необходимый формат: дд.мм.гггг чч:мм (например 07.11.2022 15:30 )",
        reply_markup=now_markup("order_start_date")
    )
    await CreateOrderStates.get_order_start_date.set()


@dp.message_handler(state=CreateOrderStates.get_order_start_date)
async def get_order_start_date(message: types.Message, state: FSMContext):
    date_time_str: str = message.text
    order_start_date_time = parse_date(date_time_str)

    if order_start_date_time is not None:
        await state.update_data(order_start_date_time=order_start_date_time.strftime("%Y-%m-%d %H:%M"))
        await message.answer(
            text="Время на выполнение задания ( выберите кнопкой или введите самостоятельно текстом)",
            reply_markup=order_execution_time_markup()
        )
        await CreateOrderStates.get_order_execution_time.set()
    else:
        await message.answer(
            text="Указан неверный формат, либо некоторые значения выходят за границы допустимого. Попробуйте еще раз"
        )


@dp.callback_query_handler(now_callback.filter(question="order_start_date"),
                           state=CreateOrderStates.get_order_start_date)
async def get_order_start_date_now(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(order_start_date_time=datetime.now().strftime("%Y-%m-%d %H:%M"))
    await callback.message.answer(
        text="Время на выполнение задания (выберите кнопкой или введите самостоятельно текстом "
             "в формате чч:мм (например 2:05))",
        reply_markup=order_execution_time_markup()
    )
    await CreateOrderStates.get_order_execution_time.set()


async def create_order(customer_telegram_id: int, state: FSMContext):
    state_data = await state.get_data()
    print(state_data)
    execution_time_str = state_data.get("order_execution_time")
    hours, minutes = execution_time_str.split(":")
    execution_time = time(int(hours), int(minutes), 0)
    customer = await CustomersModel.get_by_telegram_id(customer_telegram_id)
    category = await JobCategoriesModel.get_by_id(state_data.get("category_id"))
    location = f"{state_data.get('location').latitude} {state_data.get('location').longitude}"
    order_data = {
        "customer": customer,
        "category": category,
        "customer_name": state_data.get("customer_name"),
        "location": location,
        "customer_phone": state_data.get("phone"),
        "start_date": state_data.get("order_start_date_time"),
        "execution_time": execution_time,
        "allow_to_write_in_telegram": state_data.get("can_write")
    }
    if state_data.get("additional_contacts"):
        order_data["additional_contacts"] = state_data.get("additional_contacts")
    if state_data.get("order_description"):
        order_data["description"] = state_data.get("order_description")
    if state_data.get("order_voice_description"):
        order_data["voice_description"] = state_data.get("order_voice_description")

    order = await OrdersModel.create(**order_data)
    candidates = await get_candidates_by_filters(order, [])
    await notify_workers_about_new_order(candidates, order)


@dp.callback_query_handler(order_execution_time_callback.filter(), state=CreateOrderStates.get_order_execution_time)
async def get_order_execution_time_callback(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    execution_time = callback_data.get("time")
    await state.update_data(order_execution_time=execution_time.replace("-", ":"))
    try:
        await callback.message.answer("Ищу исполнителей...")
        await create_order(callback.from_user.id, state)
        await callback.message.answer(
            text="Заказ успешно создан и отправлен исполнителям рядом",
            reply_markup=main_markup
        )
        await state.finish()
    except Exception as e:
        print(e)
        await callback.message.answer(
            text="При создании заказа возникла непредвиденная ошибка",
            reply_markup=main_markup
        )
        await state.finish()


@dp.message_handler(state=CreateOrderStates.get_order_execution_time)
async def get_order_execution_time(message: types.Message, state: FSMContext):
    order_execution_time: str = message.text
    if correct_time(order_execution_time):
        await state.update_data(order_execution_time=order_execution_time)
        try:
            await message.answer("Ищу исполнителей...")
            await create_order(message.from_user.id, state)
            await message.answer(
                text="Заказ успешно создан и отправлен исполнителям рядом",
                reply_markup=main_markup
            )
            await state.finish()
        except Exception as e:
            print(e)
            await message.answer(
                text="При создании заказа возникла непредвиденная ошибка",
                reply_markup=main_markup
            )
            await state.finish()
    else:
        await message.answer(
            text="Время указано в неправильном формате, либо выходит за границы допустимого. Попробуйте еще раз"
        )




