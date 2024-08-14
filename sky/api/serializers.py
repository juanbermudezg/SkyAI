from rest_framework import serializers
from ..models import Flight, User, Airliner, LocationAirport, Flight_AI

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'lastname']

class AirlinerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airliner
        fields = ['id', 'name', 'path2image', 'id2ai']

class LocationAirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationAirport
        fields = ['id', 'nameAirport', 'nameCity', 'nameCountry', 'IATA_Code']

class FlightSerializer(serializers.ModelSerializer):
    airliner = AirlinerSerializer()
    from_airport = LocationAirportSerializer()
    to_airport = LocationAirportSerializer()

    class Meta:
        model = Flight
        fields = ['id', 'flight_number', 'airliner', 'year', 'month', 'day', 'hourSTD', 'minuteSTD', 'hourSTA', 'minuteSTA', 'from_airport', 'to_airport', 'user']

class FlightAISerializer(serializers.ModelSerializer):
    flight = FlightSerializer()

    class Meta:
        model = Flight_AI
        fields = ['id', 'flight', 'status_text', 'hourATD', 'minuteATD', 'hourATA', 'minuteATA']