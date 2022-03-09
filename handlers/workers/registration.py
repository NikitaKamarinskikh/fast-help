from aiogram.dispatcher import FSMContext
from aiogram import types

from keyboards.default.start import start_keyboard
from keyboards.inline.skip import skip_markup, skip_callback
from loader import dp
from keyboards.inline.chose_role import chose_role_callback, chose_role_markup
from keyboards.inline.start_or_back import start_or_back_markup, start_or_back_callback
from keyboards.inline.agree_or_not import agree_or_not_markup, agree_or_not_callback
from keyboards.inline.categories import create_categories_markup, get_category_callback, confirm_callback
from keyboards.default.main import main_markup
from keyboards.default.get_location import get_location_markup
from keyboards.default.get_phone import get_phone_markup
from data.config import Roles, MainMenuCommands
from data.config import InlineKeyboardAnswers
from models import BotUsersModel, WorkersModel, JobCategoriesModel, DocumentsModel, CustomersModel
from states.common.confirm_privacy_policy import ConfirmPrivacyPolicy
from states.workers.registration import WorkerRegistrationStates


@dp.message_handler(text="Стать помощником")
async def start_worker_registration(message: types.Message, state: FSMContext):
    await message.answer(
        text="Для того чтобы стать помощником понадобится заполнить небольшую анкету и "
             "согласиться с хранением и обработкой данных",
        reply_markup=start_or_back_markup(Roles.worker)
    )
    await ConfirmPrivacyPolicy.ask_to_confirm.set()


@dp.callback_query_handler(start_or_back_callback.filter(choice=InlineKeyboardAnswers.get_back, role=Roles.worker),
                           state=ConfirmPrivacyPolicy.ask_to_confirm)
async def ask_to_confirm_privacy_policy(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.finish()
    customer = await CustomersModel.get_or_none(callback.from_user.id)
    if customer:
        await callback.message.answer(
            text="Главное меню",
            reply_markup=main_markup
        )
    else:
        await callback.message.answer(
            text="Добро пожаловать\nВы ищите помощь или хотите стать помощником?",
            reply_markup=start_keyboard
        )


@dp.callback_query_handler(start_or_back_callback.filter(choice=InlineKeyboardAnswers.start, role=Roles.worker),
                           state=ConfirmPrivacyPolicy.ask_to_confirm)
async def ask_to_confirm_privacy_policy(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    documents = await DocumentsModel.get_by_user_category("workers")
    for document in documents:
        await callback.message.answer_document(document.telegram_id)
    await callback.message.answer(
        text="Прочитайте и подтвердите согласие",
        reply_markup=agree_or_not_markup(Roles.worker)
    )
    await ConfirmPrivacyPolicy.get_answer.set()


@dp.callback_query_handler(agree_or_not_callback.filter(choice=InlineKeyboardAnswers.agree, role=Roles.worker),
                           state=ConfirmPrivacyPolicy.get_answer)
async def confirm_privacy_policy(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.finish()
    await callback.message.answer(
        text="Как к вам должны обращаться заказчики? (Введите имя или имя отчество)",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await WorkerRegistrationStates.get_name.set()
    await state.update_data(update=False)


@dp.callback_query_handler(agree_or_not_callback.filter(choice=InlineKeyboardAnswers.do_not_agree, role=Roles.worker),
                           state=ConfirmPrivacyPolicy.get_answer)
async def confirm_privacy_policy(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(
        text="Для того чтобы стать помощником понадобится заполнить небольшую анкету и "
             "согласиться с хранением и обработкой данных",
        reply_markup=start_or_back_markup(Roles.worker)
    )
    await ConfirmPrivacyPolicy.ask_to_confirm.set()


@dp.message_handler(state=WorkerRegistrationStates.get_name)
async def get_name(message: types.Message, state: FSMContext):
    categories: list = await JobCategoriesModel.get_all()
    await state.update_data(categories_list=categories)
    name: str = message.text
    await state.update_data(worker_name=name)
    await state.update_data(categories=set())
    await message.answer(
        text="Выберите категории в которых вы хотите оказывать помощь",
        reply_markup=create_categories_markup(categories, confirm_button=True)
    )
    await WorkerRegistrationStates.get_category.set()


def get_category_by_id(categories: list, id_: int):
    for category in categories:
        if category.pk == id_:
            return category


@dp.callback_query_handler(get_category_callback.filter(), state=WorkerRegistrationStates.get_category)
async def get_category_id(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    category_id = callback_data.get("category_id")
    state_data = await state.get_data()
    categories_list = state_data.get("categories_list")
    categories = state_data.get("categories")
    categories.add(category_id)
    await state.update_data(categories=categories)

    text = "Выберите категории в которых вы хотите оказывать помощь\nВыбранные категории:\n"
    for category in enumerate(categories):
        text += f"{category[0] + 1}) {get_category_by_id(categories_list, int(category[1])).name}\n"
    await callback.message.edit_text(
        text=text,
        reply_markup=create_categories_markup(categories_list, confirm_button=True)
    )


@dp.callback_query_handler(confirm_callback.filter(), state=WorkerRegistrationStates.get_category)
async def get_category(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    categories = state_data.get("categories")
    if len(categories):
        await callback.message.answer(
            text="Отправьте вашу локацию (регистрироваться лучше там, где вы проводите большую часть дня, "
                 "для того, чтобы вам приходили уведомления о заданиях рядом)",
            reply_markup=get_location_markup
        )
        await WorkerRegistrationStates.get_location.set()
    else:
        await callback.message.answer("Необходимо выбрать минимум 1 категорию")


@dp.message_handler(content_types=types.ContentTypes.LOCATION, state=WorkerRegistrationStates.get_location)
async def get_location(message: types.Message, state: FSMContext):
    location = message.location  # {"latitude": 10.123123, "longitude": 23.44233}
    await state.update_data(location=location)
    await message.answer(
        text="Отправьте ваш телефон",
        reply_markup=get_phone_markup
    )
    await WorkerRegistrationStates.get_phone.set()


@dp.message_handler(content_types=types.ContentTypes.CONTACT, state=WorkerRegistrationStates.get_phone)
async def get_phone(message: types.Message, state: FSMContext):
    if message.contact.user_id == message.from_user.id:
        phone: str = message.contact.phone_number
        await state.update_data(phone=phone)
        await message.answer(
            text="Телефон принят",
            reply_markup=types.ReplyKeyboardRemove()
        )
        await message.answer(
            text="Вы хотите указать дополнительные контакты? Если да - введите всю информацию в строке ввода. "
                 "Если нет нажмите кнопку пропустить",
            reply_markup=skip_markup("worker_has_additional_contacts")
        )
        await WorkerRegistrationStates.get_additional_contacts.set()
    else:
        await message.answer("Похоже, вы использовали чужой номер телефона. Воспользуйтесь кнопкой, чтобы отправить "
                             "свой номер телефона")


@dp.message_handler(state=WorkerRegistrationStates.get_phone)
async def get_phone_by_message(message: types.Message):
    await message.answer("Чтобы отправить номер телефона, воспользуйтесь кнопкой ниже")


async def save_worker_data(worker_telegram_id: int, state: FSMContext):
    state_data = await state.get_data()
    categories_list = state_data.get("categories_list")
    user = await BotUsersModel.get_by_telegram_id(worker_telegram_id)
    location = f"{state_data.get('location').latitude} {state_data.get('location').longitude}"
    update = state_data.get("update")
    worker_data = {
        "user": user,
        "name": state_data.get("worker_name"),
        "telegram_id": worker_telegram_id,
        "location": location,
        "phone": state_data.get("phone"),
        "is_privacy_policy_confirmed": True
    }
    if state_data.get("additional_contacts"):
        worker_data["additional_contacts"] = state_data.get("additional_contacts")

    if update:
        worker = await WorkersModel.get_by_telegram_id(worker_telegram_id)
        del worker_data["user"]
        await WorkersModel.update_worker_by_id(worker.pk, **worker_data)
    else:
        worker = await WorkersModel.create_worker(**worker_data)

    categories = list()
    for category_id in state_data.get("categories"):
        categories.append(get_category_by_id(categories_list, int(category_id)))
    await WorkersModel.add_categories_to_worker(worker, categories)


@dp.callback_query_handler(skip_callback.filter(question="worker_has_additional_contacts"),
                           state=WorkerRegistrationStates.get_additional_contacts)
async def has_additional_contacts_skip(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    await state.update_data(additional_contacts=None)
    await save_worker_data(callback.from_user.id, state)
    if state_data.get("update"):
        await callback.message.answer(
            text="Данные успешно изменены",
            reply_markup=main_markup
        )
    else:
        await callback.message.answer(
            text="Вы завершили регистрацию в боте. Как только рядом с вами появятся задания из выбранных категорий, "
                 "вы  получите уведомление.",
            reply_markup=main_markup
        )
    await state.finish()


@dp.message_handler(state=WorkerRegistrationStates.get_additional_contacts)
async def has_additional_contacts(message: types.Message, state: FSMContext):
    additional_contacts: str = message.text
    await state.update_data(additional_contacts=additional_contacts)
    await save_worker_data(message.from_user.id, state)
    state_data = await state.get_data()
    if state_data.get("update"):
        await message.answer(
            text="Данные успешно изменены",
            reply_markup=main_markup
        )
    else:
        await message.answer(
            text="Вы завершили регистрацию в боте. Как только рядом с вами появятся задания из выбранных категорий, "
                 "вы  получите уведомление.",
            reply_markup=main_markup
        )
    await state.finish()




