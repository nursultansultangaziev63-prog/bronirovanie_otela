from rest_framework import viewsets

from .models import Hotel, Room, Client, Service, Booking
from .serializers import (
    HotelSerializer, RoomSerializer, ClientSerializer, ServiceSerializer, BookingSerializer
)


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.select_related("hotel").all()
    serializer_class = RoomSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related("client", "room", "room__hotel").prefetch_related("services").all()
    serializer_class = BookingSerializer
