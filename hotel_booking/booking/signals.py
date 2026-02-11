from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Booking


@receiver(m2m_changed, sender=Booking.services.through)
def update_booking_price(sender, instance, action, **kwargs):
    if action in ('post_add', 'post_remove', 'post_clear'):
        instance.total_price = instance.calculate_total_price()
        instance.save(update_fields=['total_price'])
