from django.db.models import Q
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

    @staticmethod
    @sync_to_async
    def get_not_completed(customer: object):
        # Item.objects.filter(Q(creator=owner) | Q(moderated=False))
        return Orders.objects.filter(Q(status=OrderStatuses.waiting_for_start) or Q(status=OrderStatuses.in_progress),
                                     customer=customer)


class OrderCandidatesModel:

    @staticmethod
    @sync_to_async
    def create(order: object, worker: object) -> object:
        order.candidates.add(worker)
        order.save()
        return order
        # return OrderCandidates.objects.create(order=order, worker=worker)

    @staticmethod
    @sync_to_async
    def get_by_order(order: object) -> list:
        return order.candidates.all()
        # return OrderCandidates.objects.filter(order=order)


