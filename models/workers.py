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
    def create_worker(**data) -> object:
        try:
            return Workers.objects.get(telegram_id=data.get("telegram_id"))
        except:
            return Workers.objects.create(**data)

    @staticmethod
    @sync_to_async
    def add_categories_to_worker(worker: object, categories: list):
        for category in categories:
            worker.categories.add(category)
        worker.save()

    @staticmethod
    @sync_to_async
    def get_by_category(category, **filters) -> list:
        candidates = list()
        workers = Workers.objects.filter(**filters)
        for worker in workers:
            if category in worker.categories.all():
                candidates.append(worker)
        return candidates

