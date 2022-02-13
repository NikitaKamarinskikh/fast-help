from asgiref.sync import sync_to_async
from admin.main.models import BotAdmins


class BotAdminsModel:

    @staticmethod
    @sync_to_async
    def get_by_telegram_id(telegram_id: int) -> object:
        return BotAdmins.objects.get(telegram_id=telegram_id)



