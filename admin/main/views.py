from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from admin.main.models import BotUsers


@csrf_exempt
def process_pay_notification(request):
    if request.method == 'POST':
        print(request)
        try:
            with open("request_data.txt", "w") as f:
                f.write(request.text)
        except:
            ...
        print(request)
        return HttpResponse({"code": 0})
    else:
        return HttpResponse("get request")


