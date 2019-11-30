import requests
from django.shortcuts import render

weatherURL = 'https://api.openweathermap.org/data/2.5/weather?id=2514256&appid=a616b07331d06ea639f3b99c87ef5830&units=metric&lang=es'


def index(request):
    response = requests.get(weatherURL)
    data = response.json()
    context = {'weather': data['weather'][0]['description'],
               'temperature': str(data['main']['temp']) + 'ºC',
               'humidity': str(data['main']['humidity']) + '%',
               }
    return render(request, 'parking/page.html', context)
