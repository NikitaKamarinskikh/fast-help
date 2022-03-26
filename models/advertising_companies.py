from asgiref.sync import sync_to_async
from admin.main.models import AdvertisingCompanies


class AdvertisingCompaniesModel:

    @staticmethod
    @sync_to_async
    def get_by_number_or_none(number: int) -> object:
        return AdvertisingCompanies.objects.filter(number=number).first()

    @staticmethod
    @sync_to_async
    def update(number: int, **update_data):
        return AdvertisingCompanies.objects.filter(number=number).update(**update_data)


