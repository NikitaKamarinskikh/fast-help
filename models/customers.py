from asgiref.sync import sync_to_async
from admin.customers.models import Customers, BotUsers


class CustomersModel:

    @staticmethod
    @sync_to_async
    def get_all() -> list:
        return Customers.objects.all()

    @staticmethod
    @sync_to_async
    def get_by_id(id_: int) -> object:
        return Customers.objects.get(pk=id_)

    @staticmethod
    @sync_to_async
    def update_by_id(id_: int, **update_data) -> None:
        Customers.objects.filter(pk=id_).update(**update_data)

    @staticmethod
    @sync_to_async
    def get_by_telegram_id(telegram_id: int) -> object:
        user = BotUsers.objects.get(telegram_id=telegram_id)
        return Customers.objects.get(user=user)

    @staticmethod
    @sync_to_async
    def get_or_none(telegram_id: int) -> object:
        user = BotUsers.objects.filter(telegram_id=telegram_id).first()
        return Customers.objects.filter(user=user).first()

    @staticmethod
    @sync_to_async
    def create_customer(user: object) -> object:
        try:
            return Customers.objects.get(telegram_id=user.telegram_id)
        except:
            return Customers.objects.create(user=user, is_privacy_policy_confirmed=True)

    @staticmethod
    @sync_to_async
    def reset_privacy_policy() -> None:
        Customers.objects.filter().update(is_privacy_policy_confirmed=False)

