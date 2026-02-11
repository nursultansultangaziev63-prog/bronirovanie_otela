from django.urls import path
from .views import (
    index, room_detail, book_room, 
    booking_success, about, contact
)

urlpatterns = [
    path('', index, name='index'),
    path('rooms/<int:pk>/', room_detail, name='room_detail'),
    path('rooms/<int:pk>/book/', book_room, name='book_room'),
    path('booking/<int:pk>/success/', booking_success, name='booking_success'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
]
