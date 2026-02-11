from rest_framework import serializers
from .models import Hotel, Room, Booking, Client, Service
from django.db.models import Q

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    hotel_name = serializers.ReadOnlyField(source='hotel.name')
    
    class Meta:
        model = Room
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()
    client_name = serializers.ReadOnlyField(source='client.__str__')
    room_details = serializers.ReadOnlyField(source='room.__str__')

    class Meta:
        model = Booking
        fields = '__all__'

    def validate(self, data):
        """
        Check room availability and dates.
        """
        room = data.get('room')
        check_in = data.get('check_in')
        check_out = data.get('check_out')

        if check_in >= check_out:
            raise serializers.ValidationError("Check-out date must be after check-in date.")

        # Check for overlapping bookings
        overlapping_bookings = Booking.objects.filter(
            room=room,
            status='confirmed'
        ).filter(
            Q(check_in__lt=check_out, check_out__gt=check_in)
        )

        if self.instance:
            overlapping_bookings = overlapping_bookings.exclude(pk=self.instance.pk)

        if overlapping_bookings.exists():
            raise serializers.ValidationError("This room is already booked for the selected dates.")

        return data
