from django.db import models

class Airports(models.Model):
    city_name = models.CharField(max_length=200)
    airport_name = models.CharField(max_length=200)

class Planes(models.Model):
    plane = models.CharField(max_length=200)
    capacity = models.IntegerField()

class Carriers(models.Model) :
    company = models.CharField(max_length=200)
    raiting = models.IntegerField()

class Flights(models.Model):
    origin_city = models.CharField(max_length=200)
    origin_airport = models.CharField(max_length=200)
    dest_city = models.CharField(max_length=200)
    dest_airport = models.CharField(max_length=200)
    datetime = models.DateTimeField()
    price = models.FloatField()
    carrier = models.CharField(max_length=200)
    flight_class = models.CharField(max_length=200)
    plane_type = models.CharField(max_length=200)
    reserved = models.IntegerField()
