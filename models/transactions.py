from asgiref.sync import sync_to_async
from admin.orders.models import Orders, OrdersTimestamps
from admin.main.models import JobCategories
from admin.transactions.models import Transactions


class TransactionsModel:

    @staticmethod
    @sync_to_async
    def create(bot_user: object, amount: int) -> object:
        return Transactions.objects.create(bot_user=bot_user, amount=amount)

    @staticmethod
    @sync_to_async
    def get_by_id(id_: int):
        return Transactions.objects.get(id=id_)

    @staticmethod
    @sync_to_async
    def update(id_: int, **update_data):
        Transactions.objects.filter(id=id_).update(**update_data)


