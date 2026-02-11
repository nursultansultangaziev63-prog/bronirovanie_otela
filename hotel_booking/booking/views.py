from django.shortcuts import render, get_object_or_404, redirect
from .models import Room, Hotel, Client, Booking, Service
from datetime import datetime

def index(request):
    rooms = Room.objects.all()
    return render(request, 'booking/index.html', {'rooms': rooms})

def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'booking/room_detail.html', {'room': room})

def book_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        check_in_str = request.POST.get('check_in')
        check_out_str = request.POST.get('check_out')
        service_ids = request.POST.getlist('services')

        client, created = Client.objects.get_or_create(
            email=email,
            defaults={'first_name': first_name, 'last_name': last_name, 'phone': phone}
        )

        # Convert date strings to date objects
        try:
            check_in = datetime.strptime(check_in_str, '%Y-%m-%d').date()
            check_out = datetime.strptime(check_out_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            # Fallback or error handling
            return render(request, 'booking/book_room.html', {
                'room': room, 
                'services': Service.objects.all(),
                'error': 'Invalid date format'
            })
        
        booking = Booking.objects.create(
            client=client,
            room=room,
            check_in=check_in,
            check_out=check_out
        )
        
        if service_ids:
            services = Service.objects.filter(id__in=service_ids)
            booking.services.set(services) # Triggers m2m_changed signal for price
        else:
            # Manually trigger price calculation if no services selected
            booking.total_price = booking.calculate_total_price()
            booking.save()
            
        return redirect('booking_success', pk=booking.pk)

    services = Service.objects.all()
    return render(request, 'booking/book_room.html', {'room': room, 'services': services})

def booking_success(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'booking/success.html', {'booking': booking})

def about(request):
    return render(request, 'booking/about.html')

def contact(request):
    if request.method == 'POST':
        # Here you could save to DB or send email
        # For now, just redirect with success flag
        return redirect('/contact/?sent=1')
    return render(request, 'booking/contact.html')
