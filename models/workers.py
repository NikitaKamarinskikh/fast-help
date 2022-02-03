from asgiref.sync import sync_to_async
from admin.workers.models import Workers, WorkerCategories, BotUsers
from admin.main.models import JobCategories


class WorkersModel:

    @staticmethod
    @sync_to_async
    def get_by_telegram_id(telegram_id: int) -> object:
        user = BotUsers.objects.get(telegram_id=telegram_id)
        return Workers.objects.get(user=user)

    @staticmethod
    @sync_to_async
    def create_worker(**data) -> object:
        return Workers.objects.create(**data)


class WorkerCategoriesModel:

    @staticmethod
    @sync_to_async
    def add_category(worker: object, category: object):
        WorkerCategories.objects.create(worker=worker, category=category)



