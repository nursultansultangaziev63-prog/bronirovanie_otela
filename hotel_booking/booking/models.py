from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Hotel(models.Model):
    name = models.CharField(max_length=200, default="New Hotel")
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0, validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return self.name

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    number = models.CharField(max_length=10, default="0")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ImageField(upload_to='rooms/', null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.hotel.name} - Room {self.number}"

class Client(models.Model):
    first_name = models.CharField(max_length=100, default="Guest")
    last_name = models.CharField(max_length=100, default="User")
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, default="")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Service(models.Model):
    name = models.CharField(max_length=100, default="Service")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class Booking(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    services = models.ManyToManyField(Service, blank=True)
    check_in = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_total_price(self):
        # Room price * days
        if self.check_in and self.check_out:
            days = (self.check_out - self.check_in).days
            if days <= 0:
                days = 1
            total = self.room.price * days
        else:
            total = 0
            
        # Services price
        if self.pk:
            services_total = sum(s.price for s in self.services.all())
            total += services_total
            
        return total

    def __str__(self):
        return f"Booking {self.id} for {self.client}"
