import json

import requests
from requests.auth import HTTPBasicAuth
from environs import Env

env = Env()
env.read_env()

TEST_REQUEST_URL = "https://api.cloudpayments.ru/test"
PAYMENT_URL = "https://api.cloudpayments.ru/orders/create"


def get_payment_link(amount_rub: int, description: str, user_id: int, invoice_id: int, json_data: dict):
    data = {
        "Amount": amount_rub,
        "Currency": "RUB",
        "Description": description,
        "AccountId": str(user_id),
        "InvoiceId": invoice_id,
        "JsonData": json.dumps(json_data),
    }
    # если без ssl добавить verify=False
    result = requests.post(PAYMENT_URL,
                           params=data,
                           auth=HTTPBasicAuth(env.str("PAYMENT_PUBLIC_ID"), env.str("PAYMENT_API_SECRET")))
    result = result.json()
    if result.get("Success"):
        return result.get("Model").get("Url")
    return False

