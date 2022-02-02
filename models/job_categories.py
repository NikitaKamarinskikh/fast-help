from asgiref.sync import sync_to_async
from admin.main.models import *


class JobCategoriesModel:

    @staticmethod
    @sync_to_async
    def get_all() -> list:
        return JobCategories.objects.all()




