from .models import *
from rest_framework import serializers
from admin_app.models import *
from service_app.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields='__all__'

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email','password']

class ViewServicesSerializer(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField()
    # category_name = serializers.CharField(source="category.name", read_only=True)
    service_provider_name = serializers.CharField(source="service_provider.username", read_only=True)


    class Meta:
        model = Service
        fields = ["id", "category", "service_provider", "service_provider_name", "service","price"]

    def get_image(self, obj):
        """Returns a relative media path instead of an absolute URL."""
        if obj.image:
            return f"media/{obj.image.name}"  # Ensure this returns only "media/..."
        return None  # If no image is available
    
class ViewcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields='__all__'
        

        
class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ["id","slot_start", "slot_end", "is_booked"]
from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.id")
    service_provider = serializers.ReadOnlyField(source="service_provider.id")
    service = serializers.ReadOnlyField(source="service.id")
    slot = serializers.ReadOnlyField(source="slot.id")

    class Meta:
        model = Booking
        fields = ["id", "user", "service", "service_provider", "platform_fee","slot", "booking_date", "status"]
        read_only_fields = ["id", "booking_date", "status"]
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "user", "booking", "review_text", "rating", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate(self, data):
        """✅ Ensure that the user can only review paid bookings."""
        booking = data.get("booking")
        if booking.status != "paid":
            raise serializers.ValidationError("You can only review paid bookings.")
        
        # ✅ Check if the user already submitted a review for this booking
        if Review.objects.filter(user=data["user"], booking=booking).exists():
            raise serializers.ValidationError("You have already reviewed this booking.")
        
        return data

class TblServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblService
        fields = ['id', 'service_name']
        
        
        
class ServiceProviderSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = ServiceProvider
        fields = ['id', 'username', 'image', 'price','id_proof','latitude','longitude']

    def get_price(self, obj):
        service = Service.objects.filter(service_provider=obj).first()  # Get first related service
        return service.price if service else None
    
class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'slot_start', 'slot_end']
        
class ServiceAvailableTimeSerializer(serializers.ModelSerializer):
    slot = TimeSlotSerializer(read_only=True)  # Nested serializer for slot details

    class Meta:
        model = ServiceAvailableTime
        fields = ['id', 'date', 'slot', 'is_booked']

class UserServiceSerializer(serializers.ModelSerializer):
    service_id = serializers.IntegerField(source='service.id', read_only=True)  # ID of the service
    service_name = serializers.CharField(source='service.service_name', read_only=True)  # Correct field from TblService
    price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = Service  # ✅ Correctly referencing the Service model
        fields = ["id", "service_id", "service_name", "price"]  # ✅ Define the correct fields
        
        
class UserBookingSerializer(serializers.ModelSerializer):
    service_details =UserServiceSerializer(source="service", read_only=True)
    # user_name = serializers.SerializerMethodField()
    slot_start_time = serializers.TimeField(source="slot.slot_start", read_only=True)
    slot_end_time = serializers.TimeField(source="slot.slot_end", read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            # "user_name",
            "service_details",
            "slot_start_time",
            "platform_fee",
            "slot_end_time",
            "booking_date",
            "status",
        ]

    def get_slot_start(self, obj):
        return f"{obj.slot.slot_start.strftime('%I:%M %p')} - {obj.slot.slot_end.strftime('%I:%M %p')}"
    
    # def get_user_name(self, obj):
    #     """✅ Get user's full name."""
    #     return f"{obj.user.username}" if obj.user else "N/A"
    

class ViewUserBookingSerializer(serializers.ModelSerializer):
    service_details = serializers.SerializerMethodField()
    slot_start_time = serializers.TimeField(source="slot.slot_start", read_only=True)
    slot_end_time = serializers.TimeField(source="slot.slot_end", read_only=True)

    class Meta:
        model = Booking
        fields = ["id", "service_details", "slot_start_time","platform_fee" ,"slot_end_time", "booking_date", "status"]

    def get_service_details(self, obj):
        return {
            "id": obj.service.id,
            "service_id": obj.service.service_id,
            "service_name": obj.service.service_name,
            "price": str(obj.service.price),  # Convert price to string
        }
        
    def get_slot_start(self, obj):
        return f"{obj.slot.slot_start.strftime('%I:%M %p')} - {obj.slot.slot_end.strftime('%I:%M %p')}"
    
    
class UpiPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upi
        fields = '__all__'
        
class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'
        
        
