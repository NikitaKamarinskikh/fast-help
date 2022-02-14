from asgiref.sync import sync_to_async
from admin.orders.models import Orders, OrderCandidates
from data.config import OrderStatuses


class OrdersModel:

    @staticmethod
    @sync_to_async
    def create(**data) -> object:
        return Orders.objects.create(**data)

    @staticmethod
    @sync_to_async
    def update(order_id: int, **update_data) -> None:
        Orders.objects.filter(pk=order_id).update(**update_data)

    @staticmethod
    @sync_to_async
    def get_available_by_id(id_: int) -> object:
        return Orders.objects.get(pk=id_, status=OrderStatuses.waiting_for_start)

    @staticmethod
    @sync_to_async
    def get_by_filters(**filters) -> list:
        return Orders.objects.filter(**filters)

    @staticmethod
    @sync_to_async
    def get_by_id(id_: int) -> object:
        return Orders.objects.get(pk=id_)


class OrderCandidatesModel:

    @staticmethod
    @sync_to_async
    def create(order: object, worker: object) -> object:
        return OrderCandidates.objects.create(order=order, worker=worker)

    @staticmethod
    @sync_to_async
    def get_by_order(order: object) -> list:
        return OrderCandidates.objects.filter(order=order)


