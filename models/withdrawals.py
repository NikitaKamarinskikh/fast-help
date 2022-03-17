from asgiref.sync import sync_to_async
from admin.transactions.models import Withdrawals


class WithdrawalsModel:

    @staticmethod
    @sync_to_async
    def create(order: object, bot_user: object, coins_before: int, coins: int, coins_after: int) -> object:
        return Withdrawals.objects.create(
            order=order,
            user=bot_user,
            coins_before=coins_before,
            coins=coins,
            coins_after=coins_after
        )



