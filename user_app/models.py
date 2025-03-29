from django.db import models

# Create your models here.
class User(models.Model):
    username=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    address= models.CharField(max_length=100,default="")
    password=models.CharField(max_length=100)
    phone=models.CharField(max_length=20,default="")
    


from service_app.models import *
    
from django.db import models


    

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('booked', 'Booked'),
        ('ongoing', 'Ongoing'),
        ('not arrived','Not Arrived'),
        ('completed', 'Completed'),
        ('paid', 'Paid'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name="bookings")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="bookings")
    slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name="bookings")
    booking_date = models.DateTimeField(auto_now_add=True)
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Bookings {self.id} - {self.user.username} | {self.service.name} | {self.status}"
    
    
class Upi(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="upi")
    status = models.CharField(max_length=20, default="success")
    upi_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"UPI Payment for Booking {self.booking.id} - {self.status} | Amount: {self.amount}"


class Card(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="card")
    status = models.CharField(max_length=20, default="success")
    card_holder_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=7)
    cvv = models.CharField(max_length=4)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # ✅ New field to store total amount

    def __str__(self):
        return f"Card Payment for Booking {self.booking.id} - {self.status} | Amount: {self.amount}"

from django.core.validators import MaxValueValidator, MinValueValidator

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking=models.ForeignKey(Booking,on_delete=models.CASCADE)
    review_text=models.CharField(max_length=400)
    rating = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    