import json
from requests import post
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from keyboards.inline.send_order_to_workers import send_order_to_workers_markup
from admin.main.models import BotUsers
from admin.transactions.models import Transactions
from environs import Env

env = Env()
env.read_env()
bot_token = env.str("BOT_TOKEN")


def update_order():
    ...


def get_user_by_id(user_id: int):
    return BotUsers.objects.get(pk=user_id)


def get_transaction_by_id(transaction_id: int):
    return Transactions.objects.get(pk=transaction_id)


# def set_transaction_paid_status(transaction_id: int):
#     Transactions.objects.filter(pk=transaction_id).update(is_paid=True)


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


@csrf_exempt
def process_pay_notification(request):
    if request.method == 'POST':
        user_id = request.POST.get("AccountId")
        transaction_id = request.POST.get("InvoiceId")
        data = json.loads(request.POST.get("Data"))
        order_id = data.get("order_id")
        has_order = data.get("has_order")
        coins = data.get("coins")
        distance = data.get("distance")
        data.get("with_bonus")

        transaction = get_transaction_by_id(transaction_id)
        user = get_user_by_id(user_id)
        reply_markup = None

        if not transaction.is_paid:
            transaction.is_paid = True
            transaction.save()

            # text = f"user_id: {user_id}\ntransaction_id: {transaction_id}\n" \
            #        f"order_id: {order_id}\nhas_order: {has_order}\ncoins: {coins}\n"
            text = "Оплата принята"
            if has_order:
                reply_markup = send_order_to_workers_markup(order_id, distance)
                text += "\nЧобы отправить задание исполнителям, нажмите на прикрепленную кнопку"
            else:
                current_user_coins = user.coins
                new_user_coins = current_user_coins + coins
                user.coins = new_user_coins
                user.save()
            notify_user_about_success_transaction(user.telegram_id, text, reply_markup)
        return HttpResponse({"code": 0})
    # else:
    #     return HttpResponse("get request")


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
