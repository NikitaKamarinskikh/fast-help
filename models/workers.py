from asgiref.sync import sync_to_async
from admin.workers.models import Workers, BotUsers


class WorkersModel:

    @staticmethod
    @sync_to_async
    def get_by_telegram_id(telegram_id: int) -> object:
        user = BotUsers.objects.get(telegram_id=telegram_id)
        return Workers.objects.get(user=user)

    @staticmethod
    @sync_to_async
    def create_worker(user: object) -> object:
        return Workers.objects.create(user=user)


