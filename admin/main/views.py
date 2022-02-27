from django.shortcuts import render, HttpResponse
from admin.main.models import BotUsers


def process_pay_notification(request):
    if request.method == 'POST':
        print(request)
        with open("request_data.txt", "w") as f:
            f.write(request.text)
        print(request)
        return HttpResponse({"code": 0})
    else:
        return HttpResponse("get request")


