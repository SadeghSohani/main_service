from urllib import response
from .serializers import FlightSerializer
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import Flights,Planes
from .serializers import FlightSerializer
import requests
from django.db import connection

class FlightViewSet(viewsets.ViewSet) :

    def list(self, request) : # /api/flights
        #authentication with authentication_service
        username = request.headers.get("username")
        token = request.headers.get("tocken")
        print(username)
        print(token)
        r = requests.post("http://authentication:7000/api/user/auth", headers=request.headers)
        isvalid = r.json().get("isvalid")
        print(f'{r.json()}')
        if isvalid == 1 :
            flights = Flights.objects.all()
            serializer = FlightSerializer(flights, many = True)
            return Response(serializer.data)
        else :
            return Response({
                "message" : "your tocken is not valid"
            })


    def filter(self, request) : # api/flights/filter
        #authentication with authentication_service
        r = requests.post("http://authentication:7000/api/user/auth", headers=request.headers)
        isvalid = r.json().get("isvalid")
        if isvalid == 1 :
            query = f"SELECT * FROM `flights_flights`"
            and_clause=[]
            for k in request.data :
                if k == "datetime" :
                    if request.data.get("datetime")!=None :
                        and_clause.append("`datetime` BETWEEN '%s' AND '%s'"%(request.data.get("datetime")[0],request.data.get("datetime")[1]))
                elif k == "price" :
                    if request.data.get("price")!=None :
                        and_clause.append("`price` BETWEEN '%s' AND '%s'"%(request.data.get("price")[0],request.data.get("price")[1]))
                else:
                    if request.data.get(k) != None :
                        and_clause.append("`%s` = '%s'" % (k,request.data.get(k)))
            if len(and_clause) > 0 :
                filter_query = query + " WHERE " + ' AND '.join(and_clause) + ";"
            else : 
                filter_query = query + ";"
            print(filter_query)
            flights = Flights.objects.raw(filter_query)
            serializer = FlightSerializer(flights, many=True)
            return  Response(serializer.data)
        else :
            return Response({
                "message" : "your tocken is not valid"
            })

    def create(self, request) : # api/flights
        #authentication with authentication_service
        r = requests.post("http://authentication:7000/api/user/auth", headers=request.headers)
        isvalid = r.json().get("isvalid")
        if isvalid == 1:
            serializer = FlightSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else :
            return Response({
                "message" : "your tocken is not valid"
            })

    def reserve_flight(self, request) :
        username = request.headers.get("username")
        r = requests.post("http://authentication:7000/api/user/auth", headers=request.headers)
        isvalid = r.json().get("isvalid")

        if isvalid == 1 :

            flight_id = request.data.get("flight_id")
            flight = Flights.objects.raw(f"SELECT * FROM `flights_flights` WHERE `id` = '{flight_id}'")
            flight_reserved = flight[0].reserved
            plane_type = flight[0].plane_type
            flight_capacity = Planes.objects.raw(f"SELECT * FROM flights_planes WHERE `plane` = '{plane_type}'")[0].capacity
            if flight_reserved < flight_capacity :
                r = requests.post("http://authentication:7000/api/user/reserve", json = {"username" : username, "flight_id" : flight_id}, headers=request.headers)
                if r.status_code==202 :
                    data = {
                        "id" :flight[0].id,
                        "origin_city" : flight[0].origin_city,
                        "origin_airport" : flight[0].origin_airport,
                        "dest_city" : flight[0].dest_city,
                        "dest_airport" : flight[0].dest_airport,
                        "datetime" : flight[0].datetime,
                        "price" : flight[0].price,
                        "carrier" : flight[0].carrier,
                        "flight_class" : flight[0].flight_class,
                        "plane_type" : flight[0].plane_type,
                        "reserved" : flight[0].reserved+1,
                    }
                    serializer = FlightSerializer(instance=Flights.objects.get(id = flight_id), data=data)
                    serializer.is_valid(raise_exception = True)
                    serializer.save()
                    return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
                else :
                    return Response({
                        "message" : "something wrong!please try agin."
                    })
            else :
                return Response({
                    "message" : "capacity of this flight is full."
                })
        else :
            return Response({
                "message" : "your tocken is not valid"
            })

    def get_planes_of_a_company(self, request):
        r = requests.post("http://authentication:7000/api/user/auth", headers=request.headers)
        isvalid = r.json().get("isvalid")
        if isvalid == 1 :
            carrier = request.data.get("carrier")
            cursor = connection.cursor()
            cursor.execute(f"SELECT DISTINCT `flights_flights`.`plane_type` AS id FROM `flights_flights` WHERE `carrier` = '{carrier}'")
            data = cursor
            print(data)
            return Response(data)
        else :
            return Response({
                "message" : "your tocken is not valid"
            })