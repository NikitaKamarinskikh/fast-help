import json

from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from admin.main.models import BotUsers


@csrf_exempt
def process_pay_notification(request):
    if request.method == 'POST':
        user_id = request.POST.get("AccountId")
        transaction_id = request.POST.get("InvoiceId")
        data = json.loads(request.POST.get("Data")[0])
        order_id = data.get("order_id")
        has_order = data.get("has_order")
        coins = data.get("coins")
        return HttpResponse({"code": 0})
    else:
        return HttpResponse("get request")

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
