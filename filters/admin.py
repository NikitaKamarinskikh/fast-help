from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from models import BotAdminsModel


class AdminOnly(BoundFilter):

    async def check(self, message: types.Message) -> bool:
        try:
            moderator = await BotAdminsModel.get_by_telegram_id(message.from_user.id)
            return message.from_user.id == int(moderator.telegram_id)
        except:
            return False


