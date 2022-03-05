from aiogram import types
from loader import dp
from filters.admin import AdminOnly
from models import WorkersModel, CustomersModel


@dp.message_handler(AdminOnly(), commands=["reset_workers_privacy_policy"])
async def reset_workers_privacy_policy(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        await WorkersModel.reset_privacy_policy()
        await message.answer("Политика конфиденциальности исполнителей успешно изменена")


@dp.message_handler(AdminOnly(), commands=["reset_customers_privacy_policy"])
async def reset_customers_privacy_policy(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        await CustomersModel.reset_privacy_policy()
        await message.answer("Политика конфиденциальности заказчиков успешно изменена")

