import json

import requests
from django.shortcuts import render

weatherURL = 'https://api.openweathermap.org/data/2.5/weather?id=2514256&appid=a616b07331d06ea639f3b99c87ef5830&units=metric&lang=es'
apiURL = 'http://127.0.0.1:5000/api/v1/'


def index(request):
    weatherResponse = requests.get(weatherURL)
    weatherData = weatherResponse.json()

    parkingsResponse = requests.get(apiURL + 'openData/parkings')
    parkingsData = parkingsResponse.json()

    locationsResponse = requests.get(apiURL + 'openData/locations')
    locationsData = json.dumps(locationsResponse.json()['features'])

    i = 1
    availableSpots = 0
    totalSpots = 0
    parkingList = []

    for item in parkingsData:
        aux = ''
        info = item['availableSpotNumber']['value']

        if info == str(-1):
            aux = 'N/A'
        else:
            aux = info

        parkingList.append({'id': i,
                            'parking': item['name']['value'],
                            'available': aux,
                            'address': item['description']['value'],
                            })

        if item['availableSpotNumber']['value'] is not None and item['availableSpotNumber']['value'] != '-1':
            availableSpots += int(item['availableSpotNumber']['value'])

        if item['totalSpotNumber']['value'] != 'None' and item['totalSpotNumber']['value'] != '-1':
            totalSpots += int(item['totalSpotNumber']['value'])

        i += 1


    context = {
               'weather': weatherData['weather'][0]['description'],
               'temperature': str(weatherData['main']['temp']) + 'ºC',
               'humidity': str(weatherData['main']['humidity']) + '%',
               'parkingList': parkingList,
               'counter': i - 1,
               'totalSpots': totalSpots,
               'availableSpots': availableSpots,
               'locationsData': locationsData,
               }

    return render(request, 'parking/page.html', context)


def details(request, idParking):
    context = {
                'id': idParking,
               }
    return render(request, 'parking/parkingDetails.html', context)
