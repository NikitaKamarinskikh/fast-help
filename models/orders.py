from asgiref.sync import sync_to_async
from admin.orders.models import Orders, OrderCandidates


class OrdersModel:

    @staticmethod
    @sync_to_async
    def create(**data) -> object:
        return Orders.objects.create(**data)

    @staticmethod
    @sync_to_async
    def get_available_by_id(id_: int) -> object:
        return Orders.objects.get(pk=id_)

    @staticmethod
    @sync_to_async
    def get_by_filters(**filters):
        return Orders.objects.filter(**filters)


class OrderCandidatesModel:

    @staticmethod
    @sync_to_async
    def create(order: object, worker: object) -> object:
        return OrderCandidates.objects.create(order=order, worker=worker)

