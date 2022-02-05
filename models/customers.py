from asgiref.sync import sync_to_async
from admin.customers.models import Customers, BotUsers


class CustomersModel:

    @staticmethod
    @sync_to_async
    def get_by_telegram_id(telegram_id: int) -> object:
        user = BotUsers.objects.get(telegram_id=telegram_id)
        return Customers.objects.get(user=user)

    @staticmethod
    @sync_to_async
    def create_customer(user: object) -> object:
        try:
            return Customers.objects.get(telegram_id=user.telegram_id)
        except:
            return Customers.objects.create(user=user)


