import json

import requests
from requests.auth import HTTPBasicAuth
from aiogram import types

from loader import bot
from data.config import env


TEST_REQUEST_URL = env.str('TEST_PAYMENT_URL')
PAYMENT_URL = env.str('PAYMENT_URL')


def get_payment_link(amount_rub: int, description: str, user_id: int, invoice_id: int, json_data: dict):
    data = {
        "Amount": amount_rub,
        "Currency": "RUB",
        "Description": description,
        "AccountId": str(user_id),
        "InvoiceId": invoice_id,
        "JsonData": json.dumps(json_data),
    }
    result = requests.post(
        PAYMENT_URL,
       params=data,
       auth=HTTPBasicAuth(env.str("PAYMENT_PUBLIC_ID"), env.str("PAYMENT_API_SECRET"))
    )
    result = result.json()
    if result.get("Success"):
        return result.get("Model").get("Url")
    return False


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
        "prices": [types.LabeledPrice(label="руб", amount=amount_rub)]
    }


async def send_invoice(chat_id: int, title: str, description: str, payload: str,
                       amount_rub: int):
    await bot.send_invoice(
        chat_id=chat_id,
        title=title,
        description=description,
        payload=payload,
        provider_token=env.str("YOOKASSA_TOKEN"),
        start_parameter="true",
        currency="RUB",
        prices=[types.LabeledPrice(label="руб", amount=amount_rub * 100)]
    )

