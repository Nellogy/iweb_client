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

        if info == str(-1) or info is None:
            aux = 'N/A'
        else:
            aux = info
            availableSpots += int(info)
            totalSpots += int(item['totalSpotNumber']['value'])

        parkingList.append({'id': i,
                            'parking': item['name']['value'],
                            'available': aux,
                            'address': item['description']['value'],
                            })
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
    weatherResponse = requests.get(weatherURL)
    weatherData = weatherResponse.json()
    
    parkingResponse = requests.get(apiURL + 'openData/parking/' + str(idParking))
    parkingData = parkingResponse.json()

    locationResponse = requests.get(apiURL + 'openData/location/' + str(idParking))
    locationData = locationResponse.json()

    context = {
        'weather': weatherData['weather'][0]['description'],
        'temperature': str(weatherData['main']['temp']) + 'ºC',
        'humidity': str(weatherData['main']['humidity']) + '%',
        'id': idParking,
        'name': parkingData['name']['value'],
        'requiredPermit': parkingData['requiredPermit']['value'],
        'allowedVehicleType': parkingData['allowedVehicleType']['value'],
        'availableSpotNumber': parkingData['availableSpotNumber']['value'],
        'totalSpotNumber': parkingData['totalSpotNumber']['value'],
        'description': parkingData['description']['value'],
        'longitude': locationData['geometry']['coordinates'][0],
        'latitude': locationData['geometry']['coordinates'][1],
    }
    return render(request, 'parking/parkingDetails.html', context)
