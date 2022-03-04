import json
from requests import post
from environs import Env
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotFound
from keyboards.inline.send_order_to_workers import send_order_to_workers_markup
from admin.main.models import BotUsers
from admin.transactions.models import Transactions
from data.config import REFERRER_BONUS_PERCENT

env = Env()
env.read_env()
bot_token = env.str("BOT_TOKEN")


def update_order():
    ...


def count_bonus(sum_: int):
    return round(REFERRER_BONUS_PERCENT * (1/100) * sum_)


def get_user_by_id(user_id: int):
    return BotUsers.objects.get(pk=user_id)


def get_transaction_by_id(transaction_id: int):
    return Transactions.objects.get(pk=transaction_id)


def notify_user_about_success_transaction(user_telegram_id: int, text: str, reply_markup=None):
    if reply_markup:
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id=' \
              f'{user_telegram_id}&text={text}&reply_markup={reply_markup}'
    else:
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id=' \
              f'{user_telegram_id}&text={text}'
    r = post(url)
    response = json.loads(r.content.decode('utf-8'))
    print(response)


def notify_referrer(referrer_telegram_id: int, bonus: int, new_referrer_balance: int):
    text = f"Вы получаете бонус в размере {bonus} монет за пополнение одного из приглашенных вами пользователя. " \
           f"Ткущее количество монет: {new_referrer_balance}"
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id=' \
          f'{referrer_telegram_id}&text={text}'
    r = post(url)


@csrf_exempt
def process_pay_notification(request):
    if request.method == 'POST':
        user_id = 1  # request.POST.get("AccountId")
        transaction_id = request.POST.get("InvoiceId")
        data = json.loads(request.POST.get("Data"))
        order_id = data.get("order_id")
        has_order = data.get("has_order")
        coins = int(data.get("coins"))
        distance = data.get("distance")
        amount = int(data.get("Amount"))
        data.get("with_bonus")

        transaction = get_transaction_by_id(transaction_id)
        user = get_user_by_id(user_id)
        reply_markup = None

        if not transaction.is_paid:
            transaction.is_paid = True
            transaction.save()
            text = "Оплата принята"
            if has_order:
                reply_markup = send_order_to_workers_markup(order_id, distance)
                text += "\nЧобы отправить задание исполнителям, нажмите на прикрепленную кнопку"
            else:
                current_user_coins = user.coins
                new_user_coins = current_user_coins + coins
                user.coins = new_user_coins
                user.save()
                text += f"\nВаш баланс {new_user_coins} монет"
            notify_user_about_success_transaction(user.telegram_id, text, reply_markup)

            if user.referrer:
                bonus = count_bonus(amount)
                referrer = get_user_by_id(user.referrer.pk)
                new_referrer_balance = referrer.coins + bonus
                referrer.coins = new_referrer_balance
                referrer.save()
                notify_referrer(referrer.telegram_id, bonus, new_referrer_balance)

        return HttpResponse({"code": 0})
    return HttpResponseNotFound()
"""
<WSGIRequest: POST '/get_transaction'>

reques.post = <QueryDict: {'TransactionId': ['1037510691'], 'Amount': ['1.00'], 'Currency': ['RUB'], 
'PaymentAmount': ['1.00'], 'PaymentCurrency': ['RUB'], 
'OperationType': ['Payment'], 'InvoiceId': ['23'], 
'AccountId': ['1'], 'SubscriptionId': [''], 'Name': [''], 
'Email': [''], 'DateTime': ['2022-02-28 12:11:44'], 
'IpAddress': ['212.164.64.214'], 'IpCountry': ['RU'], 
'IpCity': ['Новосибирск'], 'IpRegion': ['Новосибирская область'], 
'IpDistrict': ['Сибирский федеральный округ'], 'IpLatitude': ['55.03923'], 
'IpLongitude': ['82.927818'], 'CardFirstSix': ['553691'], 
'CardLastFour': ['9750'], 'CardType': ['MasterCard'], 
'CardExpDate': ['11/22'], 'Issuer': ['TINKOFF BANK'], 
'IssuerBankCountry': ['RU'], 'Description': ['Оплата 1р для размещения задания на расстоянии 500м'], 
'AuthCode': ['A1B2C3'], 'Token': ['tk_b08211a708dc17f0cd498da774ad0'], 'TestMode': ['1'], 
'Status': ['Completed'], 'GatewayName': ['Test'], 'Data': ['{"order_id": 11, "has_order": true}'], 
'TotalFee': ['0.00'], 'CardProduct': ['TNW'], 'PaymentMethod': ['']}>


{'_encoding': 'utf-8', '_mutable': False}
"""
