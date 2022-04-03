from asgiref.sync import sync_to_async
from django.db.models import Q

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
    def get_by_category(category: list, **filters) -> list:
        return Workers.objects.filter(categories__in=category)

    @staticmethod
    @sync_to_async
    def get_by_category_and_coordinates(category: list,
                                        order_latitude: int,
                                        order_longitude: int,
                                        customer_telegram_id):
        latitude_range = [order_latitude - 1, order_latitude, order_latitude + 1]
        longitude_range = [order_longitude - 1, order_longitude, order_longitude + 1]
        return Workers.objects.filter(
            ~Q(telegram_id=customer_telegram_id),
            categories__in=category,
            latitude__in=latitude_range,
            longitude__in=longitude_range,
        )

    @staticmethod
    @sync_to_async
    def delete_all() -> None:
        Workers.objects.all().delete()

    @staticmethod
    @sync_to_async
    def reset_privacy_policy() -> None:
        Workers.objects.filter().update(is_privacy_policy_confirmed=False)

    @staticmethod
    @sync_to_async
    def get_all():
        return Workers.objects.all()
