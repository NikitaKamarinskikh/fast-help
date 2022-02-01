from aiogram.dispatcher import FSMContext
from aiogram import types
from loader import dp
from keyboards.inline.chose_role import chose_role_callback
from data.config import Roles


# @dp.callback_query_handler()
# async def start_customer_registration(callback: types.CallbackQuery):
#     await callback.answer()
#     await callback.message.answer(
#         text="Для того чтобы получить помощь понадобится заполнить небольшую анкету и согласиться с хранением "
#              "и обработкой данных и подписать договор оферту",
#     )


