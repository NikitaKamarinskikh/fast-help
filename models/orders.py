from django.db.models import Q
from asgiref.sync import sync_to_async
from admin.orders.models import Orders, OrderCandidates
from data.config import OrderStatuses
from django.db.models import Q


class OrdersModel:

    @staticmethod
    @sync_to_async
    def create(**data) -> object:
        return Orders.objects.create(**data)

    @staticmethod
    @sync_to_async
    def delete_all():
        Orders.objects.all().delete()

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
        waiting_for_start = Orders.objects.filter(status=OrderStatuses.waiting_for_start, customer=customer)
        in_progress = Orders.objects.filter(status=OrderStatuses.in_progress, customer=customer)
        return list(waiting_for_start) + list(in_progress)

    @staticmethod
    @sync_to_async
    def get_not_completed_by_categories(categories: list):
        return Orders.objects.filter(status=OrderStatuses.waiting_for_start, category__in=categories)

    @staticmethod
    @sync_to_async
    def get_not_completed_by_categories_and_coordinates(categories: list,
                                                        worker_latitude: int,
                                                        worker_longitude: int,
                                                        worker_telegram_id):
        latitude_range = [worker_latitude-1, worker_latitude, worker_latitude+1]
        longitude_range = [worker_longitude-1, worker_longitude, worker_longitude+1]
        return Orders.objects.filter(
            ~Q(customer_telegram_id=worker_telegram_id),
            status=OrderStatuses.waiting_for_start,
            category__in=categories,
            latitude__in=latitude_range,
            longitude__in=longitude_range,
        )

    @staticmethod
    @sync_to_async
    def add_candidate(order: object, worker: object) -> object:
        order.candidates.add(worker)
        order.save()
        return order

    # @staticmethod
    # @sync_to_async
    # def remove_candidates(order_id: int):
    #     order = Orders.objects.get(pk=order_id)
    #     order.candidates.remove()
    #     order.save()
    #     return order


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


