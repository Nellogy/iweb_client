import requests
from django.shortcuts import render


def homepage(request):
    return render(request, 'parking/mainView.html')
