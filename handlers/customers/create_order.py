import logging
from datetime import datetime, time
from aiogram.dispatcher import FSMContext
from aiogram import types
from data.config import OrderStatuses, distances, PaymentMethods
from handlers.payments.get_invoice import send_order_to_workers
from keyboards.inline.send_order_to_workers import send_order_to_workers_markup
from loader import dp
from keyboards.default.main import main_markup
from keyboards.inline.balance import coins_sum_markup, coins_sum_callback
from keyboards.inline.categories import create_categories_markup, get_category_callback
from keyboards.inline.yes_or_no import yes_or_no_markup, yes_or_no_callback
from keyboards.inline.skip import skip_markup, skip_callback
from keyboards.inline.now import now_markup, now_callback
from keyboards.inline.order_execution_time import order_execution_time_markup, order_execution_time_callback
from keyboards.inline.payments import chose_payment_markup, chose_payment_callback, payment_method_markup, \
    payment_method_callback
from keyboards.inline.distance import order_distance_markup, order_distance_callback
from keyboards.default.get_location import get_location_markup
from keyboards.default.get_phone import get_phone_markup
from states.customers.create_order import CreateOrderStates
from models import JobCategoriesModel, CustomersModel, OrdersModel, BotUsersModel, TransactionsModel, WithdrawalsModel
from common import parse_date, correct_time
from payments.payments import get_payment_link, get_invoice_data, send_invoice


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
        text="Отправьте вашу локацию (регистрироваться лучше там где вы проводите большую часть дня, "
             "для того чтобы вам приходили уведомления о заданиях рядом)",
        reply_markup=get_location_markup
    )
    await CreateOrderStates.get_location.set()


@dp.message_handler(content_types=types.ContentTypes.LOCATION, state=CreateOrderStates.get_location)
async def get_location(message: types.Message, state: FSMContext):
    location = message.location
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
            text="Телефон принят",
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


@dp.message_handler(state=CreateOrderStates.get_phone)
async def get_phone_by_message(message: types.Message):
    await message.answer("Чтобы отправить номер телефона, воспользуйтесь кнопкой ниже")


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
        reply_markup=types.ReplyKeyboardRemove()
    )
    await CreateOrderStates.get_order_description.set()


@dp.message_handler(state=CreateOrderStates.get_additional_contacts)
async def has_additional_contacts(message: types.Message, state: FSMContext):
    additional_contacts: str = message.text
    await message.answer(
        text="Напишите описание задачи или опишите голосом",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await CreateOrderStates.get_order_description.set()
    await state.update_data(additional_contacts=additional_contacts)


@dp.message_handler(state=CreateOrderStates.get_order_description, content_types=types.ContentTypes.VOICE)
async def get_description_by_voice(message: types.Message, state: FSMContext):
    voice_id = message.voice.file_id
    await state.update_data(order_voice_description=voice_id)
    await message.answer(
        text="Укажите дату и время начала задания. Необходимый формат: дд.мм.гггг чч:мм (например 07.11.2022 15:30)",
        reply_markup=now_markup("order_start_date")
    )
    await CreateOrderStates.get_order_start_date.set()


@dp.message_handler(state=CreateOrderStates.get_order_description)
async def get_task_description(message: types.Message, state: FSMContext):
    task_description: str = message.text
    await state.update_data(order_description=task_description)
    await message.answer(
        text="Укажите дату и время начала задания. Необходимый формат: дд.мм.гггг чч:мм (например 07.11.2022 15:30)",
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
            text="Время на выполнение задания (выберите кнопкой или введите самостоятельно текстом)",
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
    execution_time_str = state_data.get("order_execution_time")
    hours, minutes = execution_time_str.split(":")
    customer = await CustomersModel.get_by_telegram_id(customer_telegram_id)
    category = await JobCategoriesModel.get_by_id(state_data.get("category_id"))
    location = f"{state_data.get('location').latitude} {state_data.get('location').longitude}"
    execution_time = time(int(hours), int(minutes), 0)

    order_data = {
        "customer": customer,
        "category": category,
        "customer_telegram_id": customer_telegram_id,
        "category_name": category.name,
        "customer_name": state_data.get("customer_name"),
        "location": location,
        "distance": state_data.get("distance"),
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

    return await OrdersModel.create(**order_data)


@dp.callback_query_handler(order_execution_time_callback.filter(), state=CreateOrderStates.get_order_execution_time)
async def get_order_execution_time_callback(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    execution_time = callback_data.get("time")
    user = await BotUsersModel.get_by_telegram_id(callback.from_user.id)
    await state.update_data(order_execution_time=execution_time.replace("-", ":"))
    await callback.message.answer(
        text=f"Оплатите сумму {distances.short.customer_price * 2} рублей "
             f"для передачи вашего заказа исполнителям в радиусе {distances.short.meters}м. "
             f"Или {distances.middle.customer_price * 2} руб в радиусе {distances.middle.meters}м. "
             f"В данный момент мы снизили стоимость размещения в 2 раза так, что вы сможете разместить "
             f"2 задания за ту же цену."
             f"Или пополните счет для оплаты и получите бонусы. На счету {user.coins} монет"
    )
    await callback.message.answer(
        text="Выберите дистанцию для размещения задания",
        reply_markup=order_distance_markup()
    )
    await CreateOrderStates.get_distance.set()


@dp.message_handler(state=CreateOrderStates.get_order_execution_time)
async def get_order_execution_time(message: types.Message, state: FSMContext):
    order_execution_time: str = message.text
    user = await BotUsersModel.get_by_telegram_id(message.from_user.id)
    if correct_time(order_execution_time):
        await state.update_data(order_execution_time=order_execution_time)
        await message.answer(
            text=f"Оплатите сумму {distances.short.customer_price * 2} рублей "
                 f"для передачи вашего заказа исполнителям в радиусе {distances.short.meters}м. "
                 f"Или {distances.middle.customer_price * 2} руб в радиусе {distances.middle.meters}м. "
                 f"В данный момент мы снизили стоимость размещения в 2 раза так, что вы сможете разместить "
                 f"2 задания за ту же цену."
                 f"Или пополните счет для оплаты и получите бонусы. На счету {user.coins} монет"
        )
        await message.answer(
            text="Выберите дистанцию для размещения задания",
            reply_markup=order_distance_markup()
        )
        await CreateOrderStates.get_distance.set()
    else:
        await message.answer(
            text="Время указано в неправильном формате, либо выходит за границы допустимого. Попробуйте еще раз"
        )


@dp.callback_query_handler(order_distance_callback.filter(), state=CreateOrderStates.get_distance)
async def get_distance(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    distance = int(callback_data.get("distance"))
    print(distance)
    await state.update_data(distance=distance)
    user = await BotUsersModel.get_by_telegram_id(callback.from_user.id)
    use_coins_button = False
    if distance == distances.short.meters:
        if user.coins >= distances.short.customer_price:
            use_coins_button = True
    if distance == distances.middle.meters:
        if user.coins >= distances.middle.customer_price:
            use_coins_button = True
    await callback.message.answer(
        text="Выберите способ оплаты",
        reply_markup=payment_method_markup(use_coins_button)
    )
    await CreateOrderStates.get_payment_method.set()


@dp.callback_query_handler(payment_method_callback.filter(), state=CreateOrderStates.get_payment_method)
async def get_payment_method(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    distance = state_data.get("distance")
    method = callback_data.get("method")
    order = await create_order(callback.from_user.id, state)
    bot_user = await BotUsersModel.get_by_telegram_id(callback.from_user.id)
    if method == PaymentMethods.one_time:
        coins = distances.get_customer_price_by_distance(distance)
        amount = coins * 2
        transaction = await TransactionsModel.create(bot_user, amount)
        description = f"Оплата {amount}р для размещения задания на расстоянии {distance}м"
        payload = {
            "order_id": order.pk,
            "has_order": 1,
            "coins": coins * 2,
            "with_bonus": 0,
            "distance": distance,
            "transaction_id": transaction.pk
        }
        try:
            await send_invoice(callback.from_user.id, f"Номер задания: {order.pk}", description, str(payload), amount)
        except Exception as e:
            logging.exception(e)
            await callback.message.answer(
                text="При создании платежа произошла ошибка. Повторите попытку позже",
                reply_markup=main_markup
            )
        await state.finish()
    elif method == PaymentMethods.coins:
        coins = distances.get_customer_price_by_distance(distance)
        await WithdrawalsModel.create(bot_user, bot_user.coins, coins, bot_user.coins - coins)

        await BotUsersModel.remove_coins(callback.from_user.id, coins)
        await OrdersModel.update(order.pk, status=OrderStatuses.waiting_for_start)
        await callback.message.answer(
            text=f"Номер задания: {order.pk}",
            reply_markup=main_markup
        )
        await state.finish()
        await callback.message.answer("Ищу исполнителей...")
        await send_order_to_workers(order.pk, callback.from_user.id)
        await callback.message.answer(
            text="Ваше задание отправлено исполнителям рядом",
            reply_markup=main_markup
        )
    else:
        await state.update_data(order_id=order.pk)
        await callback.message.answer(
            text="Выберите один из вариантов",
            reply_markup=coins_sum_markup()
        )
        await CreateOrderStates.get_payment.set()


@dp.callback_query_handler(coins_sum_callback.filter(), state=CreateOrderStates.get_payment)
async def get_coins(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    order_id = state_data.get("order_id")
    coins = int(callback_data.get("coins"))
    amount = int(callback_data.get("amount_rub"))
    distance = int(state_data.get("distance"))
    bot_user = await BotUsersModel.get_by_telegram_id(callback.from_user.id)
    transaction = await TransactionsModel.create(bot_user, amount)

    description = f"Оплата {amount}р для размещения задания на расстоянии {distance}м"
    payload = {
        "order_id": order_id,
        "has_order": 1,
        "coins": coins,
        "with_bonus": 1,
        "distance": distance,
        "transaction_id": transaction.pk
    }

    try:
        await send_invoice(callback.from_user.id, f"Номер задания: {order_id}", description, str(payload), amount)
    except Exception as e:
        logging.exception(e)
        await callback.message.answer(
            text="При создании платежа произошла ошибка. Повторите попытку позже",
            reply_markup=main_markup
        )

    await state.finish()
