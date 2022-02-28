import json

from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from admin.main.models import BotUsers


@csrf_exempt
def process_pay_notification(request):
    if request.method == 'POST':
        print("request")
        data = json.loads(request.body)
        with open('frames.request_data', 'a', encoding='utf-8') as file:
            json.dump(data, file)
            file.write('\n')
        # print(request)
        # try:
        #     with open("request_data.txt") as f:
        #         f.write(request.POST)
        # except Exception as e:
        #     f.write(str(e))
        # try:
        #     with open("request_data.txt", "a") as f:
        #         f.write(request.POST)
        # except Exception as e:
        #     print(e)
        # try:
        #     with open("request_data.txt", "a") as f:
        #         f.write(request)
        # except Exception as e:
        #     print(e)
        # print(request)
        return HttpResponse({"code": 0})
    else:
        return HttpResponse("get request")


