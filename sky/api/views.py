from rest_framework import generics
from .serializers import UserSerializer, FlightSerializer, AirlinerSerializer, LocationAirportSerializer, FlightAISerializer
from sky.models import User, Flight, Airliner, LocationAirport, Flight_AI

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class FlightListView(generics.ListCreateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

class AirlinerListView(generics.ListCreateAPIView):
    queryset = Airliner.objects.all()
    serializer_class = AirlinerSerializer

class LocationAirportListView(generics.ListCreateAPIView):
    queryset = LocationAirport.objects.all()
    serializer_class = LocationAirportSerializer

class FlightAIListView(generics.ListCreateAPIView):
    queryset = Flight_AI.objects.all()
    serializer_class = FlightAISerializer
