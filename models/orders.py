from asgiref.sync import sync_to_async
from admin.orders.models import Orders


class OrdersModel:

    @staticmethod
    @sync_to_async
    def create(**data) -> object:
        return Orders.objects.create(**data)

