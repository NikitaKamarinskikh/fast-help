from django.shortcuts import render
from admin.main.models import BotUsers


def process_pay_notification(request):
    if request.method == 'POST':
        print(request)


