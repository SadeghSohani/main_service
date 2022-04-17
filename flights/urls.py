from django.contrib import admin
from django.urls import path

from .views import FlightViewSet

urlpatterns = [
    path('flights', FlightViewSet.as_view({
        'post' : 'list'
    })),
    path('flights/create', FlightViewSet.as_view({
        'post' : 'create'
    })),
    path('flights/filter', FlightViewSet.as_view({
        'post' : 'filter'
    })), 
    path('flights/reserve', FlightViewSet.as_view({
        'post' : 'reserve_flight'
    })), 
    path('flights/planesbycarrier', FlightViewSet.as_view({
        'post' : 'get_planes_of_a_company'
    })),   
]


