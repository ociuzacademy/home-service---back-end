from .models import *
from rest_framework import serializers
from admin_app.models import *
from user_app.models import *

# class ServiceProviderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=ServiceProvider
#         fields = ["username","email","password",'phone','image']

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=ServiceProvider
        fields=["email","password"]
class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ["id","slot_start", "slot_end", "is_booked"]

class ViewServicesSerializer(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ["id","service", "price","service_provider","category"]

    # def get_image(self, obj):
    #     """Returns a relative media path instead of an absolute URL."""
    #     if obj.image:
    #         return f"media/{obj.image.name}"  # Ensure this returns only "media/..."
    #     return None  # If no image is available


from rest_framework import serializers
from .models import *

class ServiceProviderSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)  # Allow file uploads

    class Meta:
        model = ServiceProvider
        fields = ['id', 'username', 'email', 'password', 'phone','id_proof','latitude','longitude', 'image']

    def get_image(self, obj):
        if obj.image:
            return f"media/{obj.image}"
        return None
    
class ViewServiceProviderSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ServiceProvider
        fields = ['id', 'username', 'email', 'password', 'phone', 'image','id_proof','latitude','longitude']

    def get_image(self, obj):
        if obj.image:
            return f"media/{obj.image}"
        return None
        
class ViewServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblService
        fields = ['id', 'category','service_name']   
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category']     
        
class TblServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblService
        fields = ['id', 'service_name']
        
        
class ServiceSerializer(serializers.Serializer):
    service = serializers.IntegerField(source='service.id')  # ID of the service
    service_name = serializers.CharField(source='service.service_name')  # Assuming 'name' field exists in TblService model
    price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)


class ServiceEntrySerializer(serializers.Serializer):
    service = serializers.PrimaryKeyRelatedField(queryset=TblService.objects.all())  # Expecting an ID, not a dict
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

class AddServicesSerializer(serializers.Serializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    service_provider = serializers.PrimaryKeyRelatedField(queryset=ServiceProvider.objects.all())
    services = ServiceEntrySerializer(many=True)
        
class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields='__all__'

class ViewBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        
class StatusBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'status'] 
        
class ViewNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class BookingDetailsSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source="service.service.service_name", read_only=True)
    user_name = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Booking
        fields = ["id", "service_name", "user_name", "booking_date", "status"]


class ReviewSerializer(serializers.ModelSerializer):
    booking_details = BookingDetailsSerializer(source="booking", read_only=True)

    class Meta:
        model = Review
        fields = ["id", "review_text", "rating", "booking_details", "created_at"]
        
        
class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'slot_start', 'slot_end']

class ServiceAvailableTimeSerializer(serializers.ModelSerializer):
    is_available = serializers.ReadOnlyField()  # Uses the property from the model

    class Meta:
        model = ServiceAvailableTime
        fields = ["service_provider", "date", "slot", "is_booked", "is_available"]

    def validate(self, data):
        """Ensure that the slot is not already booked on the same date."""
        service_provider = data["service_provider"]
        date = data["date"]
        slot = data["slot"]

        # Check if the slot is already booked on the same date
        if ServiceAvailableTime.objects.filter(
            service_provider=service_provider, date=date, slot=slot, is_booked=True
        ).exists():
            raise serializers.ValidationError("This slot is already booked on the selected date.")

        return data
    
class BookingSerializer(serializers.ModelSerializer):
    service_details = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    slot_start_time = serializers.TimeField(source="slot.slot_start", read_only=True)
    slot_end_time = serializers.TimeField(source="slot.slot_end", read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "user_name",
            "service_details",
            "platform_fee",
            "slot_start_time",
            "slot_end_time",
            "booking_date",
            "status",
        ]

    def get_slot_start(self, obj):
        return f"{obj.slot.slot_start.strftime('%I:%M %p')} - {obj.slot.slot_end.strftime('%I:%M %p')}"
    
    def get_user_name(self, obj):
        """✅ Get user's full name."""
        return f"{obj.user.username}" if obj.user else "N/A"
    
    def get_service_details(self, obj):
        """Get service details with category name"""
        return {
            "service": obj.service.id,
            "service_name": obj.service.service.service_name,  # ✅ Corrected this line
            "price": obj.service.price,
            "category_name": obj.service.category.category,  # ✅ Corrected for category name
        }
    
    
class SingleBookingSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.username", read_only=True)
    service_details = serializers.SerializerMethodField()
    slot_start_time = serializers.TimeField(source="slot.slot_start", read_only=True)
    slot_end_time = serializers.TimeField(source="slot.slot_end", read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "user_name",
            "service_details",
            "platform_fee",
            "slot_start_time",
            "slot_end_time",
            "booking_date",
            "status",
        ]

    def get_service_details(self, obj):
        """Get service details with category name"""
        return {
            "service": obj.service.id,
            "service_name": obj.service.service.service_name,  # ✅ Corrected this line
            "price": obj.service.price,
            "category_name": obj.service.category.category,  # ✅ Corrected for category name
        }
        
class ServiceProviderWorkSummarySerializer(serializers.ModelSerializer):
    booking_date = serializers.DateField(format="%Y-%m-%d")
    total_amount = serializers.DecimalField(source="service.price", max_digits=10, decimal_places=2)

    class Meta:
        model = Booking
        fields = ["booking_date", "total_amount"]