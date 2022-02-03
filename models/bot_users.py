from asgiref.sync import sync_to_async
from admin.main.models import BotUsers


class BotUsersModel:

    @staticmethod
    @sync_to_async
    def get_by_telegram_id(telegram_id: int) -> object:
        return BotUsers.objects.get(telegram_id=telegram_id)

    @staticmethod
    @sync_to_async
    def create_user(telegram_id: int, username: str) -> object:
        data = {
            "telegram_id": telegram_id,
        }
        if username:
            data["username"] = username
        return BotUsers.objects.create(**data)



