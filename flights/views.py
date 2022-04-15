from .serializers import FlightSerializer
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import Flights
from .serializers import FlightSerializer

class FlightViewSet(viewsets.ViewSet) :

    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #permission_classes = [permissions.IsAuthenticated]

    def list(self, request) : # /api/flights
        #flights = Flights.objects.filter(origin_city="Tehran",dest_city="Stokholms",flight_class="B",price="181")
        flights = Flights.objects.all()
        serializer = FlightSerializer(flights, many = True)
        return Response(serializer.data)
        
    def filter(self, request) : # api/flights/filter
        #request.headers.get("tocken")
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
        return Response(serializer.data)

    def create(self, request) : # api/flights
        serializer = FlightSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None) : # /api/flights/<str:id>
        pass

    def update(self, request, pk=None) : # /api/flights/<str:id>
        pass

    def destroy(self, request, pk=None) : # /api/flights/<str:id>
        pass

