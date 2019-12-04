# to start app: python manage.py startapp polls
from django.urls import path
from . import views

app_name = 'parkings'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:idParking>/', views.details, name='details'),
]
