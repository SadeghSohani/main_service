from django.contrib import admin
from django.urls import path

from .views import FlightViewSet

urlpatterns = [
    path('flights', FlightViewSet.as_view({
        'get' : 'list',
        'post' : 'create'
    })),
    path('flights/filter', FlightViewSet.as_view({
        'post' : 'filter'
    })),
    path('flights/<str:pk>', FlightViewSet.as_view({
        'get' : 'retrieve',
        'put' : 'update',
        'delete' : 'destroy'
    })),    
]


