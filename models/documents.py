from asgiref.sync import sync_to_async
from admin.main.models import Documents


class DocumentsModel:

    @staticmethod
    @sync_to_async
    def get_by_user_category(user_category: str) -> list:
        return Documents.objects.filter(users_category=user_category)




