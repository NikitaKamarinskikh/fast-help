import json

import requests
from requests.auth import HTTPBasicAuth
from environs import Env

env = Env()
env.read_env()

TEST_REQUEST_URL = "https://api.cloudpayments.ru/test"
PAYMENT_URL = "https://api.cloudpayments.ru/orders/create"


def get_payment_link(amount_rub: int, description: str, user_id: int):
    data = {
        "Amount": amount_rub,
        "Currency": "RUB",
        "Description": description,
        "AccountId": str(user_id)
    }
    # если без ssl добавить verify=False
    result = requests.post(PAYMENT_URL,
                           params=data,
                           auth=HTTPBasicAuth(env.str("PAYMENT_PUBLIC_ID"), env.str("PAYMENT_API_SECRET")))
    result = result.json()
    if result.get("Success"):
        return result.get("Model").get("Url")
    return False

# print(res)
# print(res.text)
"""
{
"Model":{"Id":"hISaCsNcf0Va9jBC", 
    "Number":1,"Amount":1.0, 
"Currency":"RUB","CurrencyCode":0, 
"Email":null,
"Phone":"",
"Description":"Тестовый запрос",
"RequireConfirmation":false,
"Url":"https://orders.cloudpayments.ru/d/hISaCsNcf0Va9jBC",
"CultureName":"ru-RU",
"CreatedDate":"\/Date(1645936146259)\/","CreatedDateIso":"2022-02-27T07:29:06", 
"PaymentDate":null,
"PaymentDateIso":null,
"StatusCode":0,
"Status":"Created",
"InternalId":13807724},
"Success":true,
"Message":null
}
"""
# print(res.json())
