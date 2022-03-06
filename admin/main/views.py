import json
from requests import post
from environs import Env
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotFound
from keyboards.inline.send_order_to_workers import send_order_to_workers_markup
from keyboards.default.main import main_markup
from admin.main.models import BotUsers
from admin.orders.models import Orders
from admin.transactions.models import Transactions
from data.config import REFERRER_BONUS_PERCENT, OrderStatuses

env = Env()
env.read_env()
bot_token = env.str("BOT_TOKEN")


def set_order_waiting_for_start_status(order_id: int):
    order = Orders.objects.get(pk=order_id)
    order.status = OrderStatuses.waiting_for_start
    order.save()


def count_bonus(sum_: float):
    return round(REFERRER_BONUS_PERCENT * (1 / 100) * sum_)


def get_user_by_id(user_id: int):
    return BotUsers.objects.get(pk=user_id)


def get_transaction_by_id(transaction_id: int):
    return Transactions.objects.get(pk=transaction_id)


def send_message(user_telegram_id):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id=' \
          f'{user_telegram_id}&text=При обработке платежа возникла ошибка'
    r = post(url)


def notify_user_about_success_transaction(user_telegram_id: int, new_user_coins: int, reply_markup=None):
    success_transaction_url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id=' \
                              f'{user_telegram_id}&text=Оплата принята\nТекущее количество монет: {new_user_coins}&' \
                              f'reply_markup={main_markup}'
    r = post(success_transaction_url)
    response = json.loads(r.content.decode('utf-8'))
    print(response)
    if reply_markup:
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id=' \
              f'{user_telegram_id}&text=&reply_markup={reply_markup}'

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
        user_id = request.POST.get("AccountId")
        user = get_user_by_id(user_id)
        try:
            transaction_id = request.POST.get("InvoiceId")
            amount = float(request.POST.get("Amount"))
            data = json.loads(request.POST.get("Data"))
            order_id = int(data.get("order_id"))
            has_order = data.get("has_order")
            coins = int(data.get("coins"))
            distance = data.get("distance")
            with_bonus = data.get("with_bonus")

            transaction = get_transaction_by_id(transaction_id)
            reply_markup = None
            new_user_coins = user.coins
            if not transaction.is_paid:
                transaction.is_paid = True
                transaction.save()
                if has_order:
                    reply_markup = send_order_to_workers_markup(order_id, distance)
                    set_order_waiting_for_start_status(order_id)
                else:
                    current_user_coins = user.coins
                    new_user_coins = current_user_coins + coins
                    user.coins = new_user_coins
                    user.save()

                notify_user_about_success_transaction(user.telegram_id, new_user_coins, reply_markup)

                if user.referrer:
                    bonus = count_bonus(amount)
                    referrer = get_user_by_id(user.referrer.pk)
                    new_referrer_balance = referrer.coins + bonus
                    referrer.coins = new_referrer_balance
                    referrer.save()
                    notify_referrer(referrer.telegram_id, bonus, new_referrer_balance)
        except Exception as e:
            try:
                send_message(user.telegram_id)
            except:
                ...
            with open("test.txt", "w") as f:
                f.write(str(e))
        return HttpResponse({"code": 0})
    return HttpResponseNotFound()


"""
<WSGIRequest: POST '/get_transaction'>order_id
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
