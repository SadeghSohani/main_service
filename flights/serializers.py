from .models import Flights
from rest_framework import serializers

class FlightSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Flights
        fields = '__all__'
