import json

from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from admin.main.models import BotUsers


@csrf_exempt
def process_pay_notification(request):
    if request.method == 'POST':
        with open('request_data.txt', 'w', encoding='utf-8') as file:
            print(request, file=file)
        return HttpResponse({"code": 0})
    else:
        return HttpResponse("get request")


