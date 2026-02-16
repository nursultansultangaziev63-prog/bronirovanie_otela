from django.urls import path
from .views import (
    index, room_detail, book_room,
    booking_success, about, contact,
    api_room_detail, RoomListAPIView,
)

urlpatterns = [
    # ✅ САЙТ
    path('', index, name='index'),
    path('rooms/<int:pk>/', room_detail, name='room_detail'),
    path('rooms/<int:pk>/book/', book_room, name='book_room'),
    path('booking/<int:pk>/success/', booking_success, name='booking_success'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),

    # ✅ API endpoints (если хочешь оставить их и тут тоже)
    path('api/rooms/', RoomListAPIView.as_view(), name='api-rooms'),
    path('api/rooms/<int:pk>/', api_room_detail, name='api_room_detail'),
]

