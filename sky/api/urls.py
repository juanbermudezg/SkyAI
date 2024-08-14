from django.urls import path
from .views import UserListView, FlightListView, AirlinerListView, LocationAirportListView, FlightAIListView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user_list'),
    path('flights/', FlightListView.as_view(), name='flight_list'),
    path('airliners/', AirlinerListView.as_view(), name='airliner_list'),
    path('locations/', LocationAirportListView.as_view(), name='location_list'),
    path('flight_ais/', FlightAIListView.as_view(), name='flight_ai_list'),
]
