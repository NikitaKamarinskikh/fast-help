from asgiref.sync import sync_to_async
from admin.workers.models import Workers, BotUsers
from admin.main.models import JobCategories


class WorkersModel:

    @staticmethod
    @sync_to_async
    def get_by_telegram_id(telegram_id: int) -> object:
        user = BotUsers.objects.get(telegram_id=telegram_id)
        return Workers.objects.get(user=user)

    @staticmethod
    @sync_to_async
    def get_by_id(id_: int) -> object:
        return Workers.objects.get(pk=id_)

    @staticmethod
    @sync_to_async
    def get_or_none(telegram_id: int) -> object:
        user = BotUsers.objects.filter(telegram_id=telegram_id).first()
        return Workers.objects.filter(user=user).first()

    @staticmethod
    @sync_to_async
    def create_worker(**data) -> object:
        try:
            return Workers.objects.get(telegram_id=data.get("telegram_id"))
        except:
            return Workers.objects.create(**data)

    @staticmethod
    @sync_to_async
    def update_worker_by_id(worker_id: int, **update_data) -> None:
        Workers.objects.filter(pk=worker_id).update(**update_data)

    @staticmethod
    @sync_to_async
    def add_categories_to_worker(worker: object, categories: list):
        worker.categories.clear()
        for category in categories:
            worker.categories.add(category)

    @staticmethod
    @sync_to_async
    def remove_all_categories(worker: object):
        worker.categories.clear()

    @staticmethod
    @sync_to_async
    def get_by_category(category, **filters) -> list:
        candidates = list()
        workers = Workers.objects.filter(**filters)
        for worker in workers:
            if category in worker.categories.all():
                candidates.append(worker)
        return candidates

