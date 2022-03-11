import json

import requests
from requests.auth import HTTPBasicAuth
from environs import Env
from loader import bot

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


def from_rub_to_kopecks(amount_rub: int):
    return int(str(amount_rub) + "00")


def get_invoice_data(chat_id: int, title: str, description: str, payload: str,
                     amount_rub: int) -> dict:
    return {
        "chat_id": chat_id,
        "title": title,
        "description": description,
        "payload": payload,
        "provider_token": env.str("YOOKASSA_TOKEN"),
        "currency": "RUB",
        "start_parameter": "test",
        "prices": [{
            "label": "Руб",
            # "amount": from_rub_to_kopecks(amount_rub)
            "amount": amount_rub
        }]
    }


async def send_invoice(chat_id: int, title: str, description: str, payload: str,
                       amount_rub: int):
    try:
        await bot.send_invoice(
            chat_id=chat_id,
            title=title,
            description=description,
            payload=payload,
            provider_token=env.str("YOOKASSA_TOKEN"),
            currency="RUB",
            prices=[{
                "label": "Руб",
                "amount": amount_rub * 1000
            }]
        )
    except Exception as e:
        print(e)
