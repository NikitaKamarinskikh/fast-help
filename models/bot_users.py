from asgiref.sync import sync_to_async
from admin.main.models import BotUsers


class BotUsersModel:

    @staticmethod
    @sync_to_async
    def get_by_telegram_id(telegram_id: int) -> object:
        return BotUsers.objects.get(telegram_id=telegram_id)

    @staticmethod
    @sync_to_async
    def get_by_telegram_id_or_none(telegram_id: int):
        return BotUsers.objects.filter(telegram_id=telegram_id).first()

    @staticmethod
    @sync_to_async
    def get_by_id(id_: int):
        return BotUsers.objects.get(pk=id_)

    @staticmethod
    @sync_to_async
    def create_user(telegram_id: int, username: str, referrer: object) -> object:
        try:
            user = BotUsers.objects.get(telegram_id=telegram_id)
            setattr(user, "already_existed", True)
        except:
            data = {
                "telegram_id": telegram_id,
            }
            if username:
                data["username"] = username
            if referrer:
                data["referrer"] = referrer
            user = BotUsers.objects.create(**data)
            setattr(user, "already_existed", False)
        return user

    @staticmethod
    @sync_to_async
    def update_user(telegram_id: int, **update_data) -> None:
        BotUsers.objects.filter(telegram_id=telegram_id).update(**update_data)

    @staticmethod
    @sync_to_async
    def add_coins(telegram_id: int, coins: int) -> object:
        user = BotUsers.objects.get(telegram_id=telegram_id)
        current_coins = user.coins
        current_coins += coins
        user.coins = current_coins
        user.save()
        return user

    @staticmethod
    @sync_to_async
    def remove_coins(telegram_id: int, coins: int) -> object:
        user = BotUsers.objects.get(telegram_id=telegram_id)
        current_coins = user.coins
        current_coins -= coins
        user.coins = current_coins
        user.save()
        return user

    @staticmethod
    @sync_to_async
    def get_referrals(user: object) -> list:
        return BotUsers.objects.filter(referrer=user)
