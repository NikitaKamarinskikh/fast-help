from asgiref.sync import sync_to_async
from admin.orders.models import Orders, OrdersTimestamps
from admin.main.models import JobCategories


class OrderTimestampsModel:

    @staticmethod
    @sync_to_async
    def set_timestamp(order: object, seconds: int) -> object:
        return OrdersTimestamps.objects.create(
            order=order,
            seconds=seconds
        )

    @staticmethod
    @sync_to_async
    def delete_timestamp(timestamp: object) -> None:
        timestamp.delete()

    @staticmethod
    @sync_to_async
    def get_by_id(id_: int) -> object:
        return OrdersTimestamps.objects.get(pk=id_)

    @staticmethod
    @sync_to_async
    def get_all() -> list:
        return OrdersTimestamps.objects.all()

    @staticmethod
    @sync_to_async
    def get_by_order(order: object) -> object:
        return OrdersTimestamps.objects.get(order=order)

    @staticmethod
    @sync_to_async
    def delete_by_order(order: object) -> None:
        OrdersTimestamps.objects.filter(order=order).delete()




