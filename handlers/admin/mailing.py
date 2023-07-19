import logging
from typing import List

from aiogram import types
from loader import dp, bot

from filters.admin import AdminOnly
from models import WorkersModel, CustomersModel, BotUsersModel


@dp.message_handler(AdminOnly(), commands=["send_message_to_workers"])
async def send_message_to_workers(message: types.Message):
    workers = await WorkersModel.get_all()
    text = "test message for workers"
    await message.answer("start sending messages")
    await _send_message_for_users_list(workers,text)
    await message.answer("finish sending messages")


@dp.message_handler(AdminOnly(), commands=["send_message_to_customers"])
async def send_message_to_customers(message: types.Message):
    customers = await CustomersModel.get_all()
    text = "test message for customers"
    await message.answer("start sending messages")
    await _send_message_for_users_list(customers, text)
    await message.answer("finish sending messages")


@dp.message_handler(AdminOnly(), commands=["send_message_to_all_bot_users"])
async def send_message_to_all_bot_users(message: types.Message):
    users = await BotUsersModel.get_all()
    text = "test message for all users"
    await message.answer("start sending messages")
    await _send_message_for_users_list(users, text)
    await message.answer("finish sending messages")


async def _send_message_for_users_list(users, text: str) -> None:
    for user in users:
        try:
            await bot.send_message(
                chat_id=user.telegram_id,
                text=text
            )
        except Exception as e:
            logging.exception(e)

