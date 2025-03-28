from django.db import models
from admin_app.models import *

# Create your models here.
# class ServiceProvider(models.Model):
#     username = models.CharField(max_length=100)
#     email = models.CharField(max_length=100)
#     password = models.CharField(max_length=50)
#     phone = models.CharField(max_length=20)
#     company_name = models.CharField(max_length=100)
#     is_approved = models.BooleanField(default=False)
#     status = models.CharField(max_length=100, default="pending")
    
#     def __str__(self):
#         # This makes sure that when a ServiceProvider is printed (or serialized using StringRelatedField),
#         # you see the username instead of "ServiceProvider object (1)".
#         return self.username

# class ServiceSlot(models.Model):
#     service = models.ForeignKey(Services, on_delete=models.CASCADE, related_name='slots')
#     start_time = models.TimeField()
#     end_time = models.TimeField()
#     is_booked = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.service.name}: {self.start_time} - {self.end_time}"
from django.db import models
from datetime import datetime, timedelta

# class ServiceProvider(models.Model):
#     username = models.CharField(max_length=100)
#     email = models.CharField(max_length=100)
#     password = models.CharField(max_length=50)
#     phone = models.CharField(max_length=20)
#     company_name = models.CharField(max_length=100)
#     is_approved = models.BooleanField(default=False)
#     status = models.CharField(max_length=100, default="pending")
    
#     def __str__(self):
#         # This makes sure that when a ServiceProvider is printed (or serialized using StringRelatedField),
#         # you see the username instead of "ServiceProvider object (1)".
#         return self.username
from django.db import models
from datetime import datetime, timedelta

class ServiceProvider(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),                   # After registration, before approval/review
        ('services_not_added', 'Services Not Added'),  # Registered but skipped service addition
        ('services_added', 'Services Added'),         # Services were added successfully
        ('approved', 'Approved'),                     # Admin manually approves
        ('rejected', 'Rejected'),                     # Admin manually rejects
    ]
    
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    image = models.ImageField(upload_to="service_provider_image", null=True, blank=True)
    id_proof =models.ImageField(upload_to='id_proof',null=True,blank=True)
    password = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=11, decimal_places=7,default=0.0)
    longitude=models.DecimalField(max_digits=11, decimal_places=7,default=0.0)
    is_approved = models.BooleanField(default=False)
    status = models.CharField(max_length=100, default="services_not_added")
    
    def generate_slots(self):
        """Generates 3-hour slots for a 24-hour period after approval."""
        if self.is_approved and not TimeSlot.objects.filter(service_provider=self).exists():
            start_time = datetime.strptime("00:00", "%H:%M")
            for i in range(0, 24, 3):  # 3-hour interval
                slot_start = start_time + timedelta(hours=i)
                slot_end = slot_start + timedelta(hours=3)
                TimeSlot.objects.create(
                    service_provider=self,
                    slot_start=slot_start.time(),
                    slot_end=slot_end.time()
                )

    def save(self, *args, **kwargs):
        is_newly_approved = self.pk and not ServiceProvider.objects.get(pk=self.pk).is_approved and self.is_approved
        super().save(*args, **kwargs)
        
        if is_newly_approved:
            self.generate_slots()

class TimeSlot(models.Model):
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    slot_start = models.TimeField()
    slot_end = models.TimeField()


class ServiceAvailableTime(models.Model):
    service_provider = models.ForeignKey(
        ServiceProvider, 
        on_delete=models.CASCADE, 
        related_name='service_provider_available_time'
    )
    date = models.DateField()
    slot=models.ForeignKey(TimeSlot,on_delete=models.CASCADE)
    is_booked = models.BooleanField(default=False) 
    
    def is_available(self):
        """Returns True if the slot is not booked."""
        return not self.is_booked

    # def create_slots(self, slot_duration=180):
    #     start_dt = datetime.combine(self.date, self.start_time)
    #     end_dt = datetime.combine(self.date, self.end_time)
    #     slot_delta = timedelta(minutes=slot_duration)

    #     slots = []
    #     while start_dt + slot_delta <= end_dt:
    #         slot_end_dt = start_dt + slot_delta
    #         slots.append(Slots(
    #             service_available_time=self,
    #             date=self.date,
    #             start_time=start_dt.time(),
    #             end_time=slot_end_dt.time(),
    #             status="available"
    #         ))
    #         start_dt += slot_delta

    #     Slots.objects.bulk_create(slots)
        
# class Slots(models.Model):
#     STATUS_CHOICES = [
#         ('available', 'Available'),
#         ('booked', 'Booked'),
#         ('cancelled', 'Cancelled'),
#     ]
    
#     service_available_time = models.ForeignKey(
#         ServiceAvailableTime, 
#         on_delete=models.CASCADE, 
#         related_name='slots'
#     )
#     date = models.DateField()
#     start_time = models.TimeField()
#     end_time = models.TimeField()
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    
#     def __str__(self):
#         return f"{self.date} | {self.start_time} - {self.end_time} | {self.status}"


class Service(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    service_provider=models.ForeignKey(ServiceProvider,on_delete=models.CASCADE)
    service = models.ForeignKey(TblService,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)