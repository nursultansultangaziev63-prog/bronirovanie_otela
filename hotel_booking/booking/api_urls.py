from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import api_root
from .api import HotelViewSet, RoomViewSet, ClientViewSet, ServiceViewSet, BookingViewSet

router = DefaultRouter()
router.register(r"hotels", HotelViewSet, basename="hotels")
router.register(r"rooms", RoomViewSet, basename="rooms")
router.register(r"clients", ClientViewSet, basename="clients")
router.register(r"services", ServiceViewSet, basename="services")
router.register(r"bookings", BookingViewSet, basename="bookings")

urlpatterns = [
    path("", api_root, name="api_root"),
    path("", include(router.urls)),
]
