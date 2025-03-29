
from django.shortcuts import get_object_or_404, render,redirect
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status,viewsets,generics
from rest_framework.views import APIView
from admin_app.models import *
from service_app.models import *
from service_app.models import *
# Create your views here.


class UserRegistrationView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            response_data = {
                "status": "success",
                "message": "User created successfully",
                "data": serializer.data  # This will show the saved user data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "status": "failed",
                "message": "Invalid Details",
                "errors": serializer.errors,  # Optionally show validation errors
                "data": request.data  # This will show the data that was sent
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            email = request.data.get('email')
            password = request.data.get('password')

            try:
                user = User.objects.get(email=email)
                # ⚠️ This is insecure (plaintext password check); it's better to use Django's `check_password()` if passwords are hashed.
                if password == user.password:
                    response_data = {
                        "status": "success",
                        "message": "User logged in successfully",
                        "user_id": str(user.id),
                        "data": request.data  # Show the sent data
                    }
                    request.session['id'] = user.id
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "status": "failed",
                        "message": "Invalid credentials",
                        "data": request.data  # Show the sent data
                    }, status=status.HTTP_401_UNAUTHORIZED)

            except User.DoesNotExist:
                return Response({
                    "status": "failed",
                    "message": "User not found",
                    "data": request.data  # Show the sent data
                }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "status": "failed",
            "message": "Invalid input",
            "errors": serializer.errors,  # Helpful to see exactly what validation failed
            "data": request.data  # Show the sent data
        }, status=status.HTTP_400_BAD_REQUEST)
    

# class ViewServicesView(viewsets.ReadOnlyModelViewSet):
#     queryset = Services.objects.all()
#     serializer_class = ViewServiceSerializer

#     def list(self, request, *args, **kwargs):
#         service_id = request.query_params.get("id")  # Fetch service_id from query params

#         if service_id:
#             try:
#                 service = self.queryset.get(id=service_id)
#                 serializer = self.get_serializer(service,many=True)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             except Services.DoesNotExist:
#                 return Response({"detail": "Service not found."}, status=status.HTTP_404_NOT_FOUND)
#         else:
#             # No filtering, return all services
#             return super().list(request, *args, **kwargs)
            

class UpdateProfileview(generics.UpdateAPIView):
    serializer_class=UserSerializer 
    queryset=User.objects.all()
    http_method_names=['patch']

    def update(self, request, *args, **kwargs):
        user_id= request.data.get('id')
        if not user_id:
            return Response({"detail": "Service Provider ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the service instance using the provided service_id
           user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Update the Service instance with the provided data
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({"detail": "Profile updated successfully.", "service": serializer.data}, status=status.HTTP_200_OK)
    
class ViewCategoryView(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = ViewcategorySerializer

    def  list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
class ServiceByCategoryView(viewsets.ReadOnlyModelViewSet):
    serializer_class = TblServiceSerializer
    queryset = TblService.objects.all()

    def list(self, request, *args, **kwargs):
        category_id = request.query_params.get('category_id')
        if category_id:
            queryset = self.get_queryset().filter(category_id=category_id)
        else:
            queryset = self.get_queryset()

        if not queryset.exists():
            return Response({"message": "No services found for the given category."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# class CustomerSupportView(viewsets.ModelViewSet):  
#     queryset = CustomerSupport.objects.all()
#     serializer_class = CustomerSupportSerializer
#     http_method_names=['post']

#     def post(self, request):
#         try:
            
#             serializer = CustomerSupportSerializer(data=request.data)
#             print(request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response({"message": "Service added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
#             return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class BrowseServicesView(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ViewServicesSerializer
    http_method_names=['get']
    def list(self, request, *args, **kwargs):
        name = request.query_params.get('name', None)
        print("Query parameter received:", name)  # Debugging
        
        if name:
            services = Service.objects.filter(name__icontains=name)
            print("Filtered services:", services)  # Debugging
        else:
            services = Service.objects.all()
            print("All services:", services)  # Debugging

        serializer = self.get_serializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# class AvailableSlotsViewSet(viewsets.ViewSet):
#     def list(self, request):
#         service_available_time_id = request.query_params.get("service_available_time_id")

#         if not service_available_time_id:
#             return Response({"error": "Service Available Time ID is required."}, status=status.HTTP_400_BAD_REQUEST)

#         slots = Slots.objects.filter(service_available_time_id=service_available_time_id, status="available")

#         serializer = SlotSerializer(slots, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    

# class BookingViewSet(viewsets.ModelViewSet):
#     queryset = Bookings.objects.all()
#     serializer_class = BookingSerializer
#     http_method_names=['post']

#     def create(self, request, *args, **kwargs):
#         user_id = request.data.get("user")
#         service_provider_id = request.data.get("service_provider")
#         service_id = request.data.get("service")
#         slot_id = request.data.get("slot")

#         slot = get_object_or_404(Slots, id=slot_id)

#         if slot.status != "available":
#             return Response({"error": "Slot is not available"}, status=status.HTTP_400_BAD_REQUEST)

#         # Create booking
#         booking = Bookings.objects.create(
#             user_id=user_id,
#             service_provider_id=service_provider_id,
#             service_id=service_id,
#             slot_id=slot_id,
#             status="pending"
#         )

#         # Update slot status
#         slot.status = "booked"
#         slot.save()

#         return Response({"message": "Slot booked successfully", "booking_id": booking.id}, status=status.HTTP_201_CREATED)

class BookingHistoryViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    http_method_names = ['get']
    
    def booking_history(self, request):
        user_id = request.query_params.get("user_id")

        if not user_id:
            return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        bookings = Booking.objects.filter(user_id=user_id).select_related("service", "service_provider", "slot")

        if not bookings.exists():
            return Response({"message": "No booking history found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateReviewView(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        # ✅ Get user_id and booking_id from request data
        user_id = request.data.get("user_id")
        booking_id = request.data.get("booking_id")

        # ✅ Validate user_id and booking_id
        if not user_id or not booking_id:
            return Response(
                {"status": "failed", "message": "User ID and Booking ID are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ✅ Check if the booking exists and belongs to the user
        try:
            booking = Booking.objects.get(id=booking_id, user_id=user_id)
        except Booking.DoesNotExist:
            return Response(
                {"status": "failed", "message": "Booking not found or does not belong to the user."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # ✅ Validate that the booking is paid
        if booking.status != "paid":
            return Response(
                {"status": "failed", "message": "You can only review paid bookings."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ✅ Check if the user has already reviewed this booking
        if Review.objects.filter(user_id=user_id, booking_id=booking_id).exists():
            return Response(
                {"status": "failed", "message": "You have already reviewed this booking."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ✅ Create a mutable copy of request.data
        mutable_data = request.data.copy()
        mutable_data["user"] = user_id
        mutable_data["booking"] = booking_id

        # ✅ Create the review
        serializer = self.get_serializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save(user_id=user_id, booking_id=booking_id)
            return Response(
                {"status": "success", "message": "Review created successfully.", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"status": "failed", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

class ViewUserProfileView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get("id")  # Get user id from query parameters

        if user_id:
            try:
                user = self.queryset.get(id=user_id)
                serializer = self.get_serializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            # No user_id provided, return all users (if required)
            return super().list(request, *args, **kwargs)
        
        
class ServiceProviderViewSet(viewsets.ViewSet):
    """
    View to get providers offering a specific service.
    """
    def list(self, request, *args, **kwargs):
        service_id = request.query_params.get('service_id')

        if not service_id:
            return Response({"error": "service_id parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            service_providers = ServiceProvider.objects.filter(service__id=service_id, is_approved=True)
        except Exception as e:
            return Response({"error": "Invalid service_id or providers not found."}, status=status.HTTP_404_NOT_FOUND)

        if not service_providers.exists():
            return Response({"message": "No providers found for this service."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ServiceProviderSerializer(service_providers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
from math import radians, cos, sin, sqrt, atan2
from django.db.models import F
    
# def haversine(lat1, lon1, lat2, lon2):
#     """Calculate the distance between two points on the Earth using the Haversine formula."""
#     R = 6371  # Radius of the Earth in km
#     lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
#     dlat = lat2 - lat1
#     dlon = lon2 - lon1

#     a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
#     c = 2 * atan2(sqrt(a), sqrt(1-a))

#     return R * c  # Distance in km

# class NearestServiceProviders(APIView):
#     def get(self, request, *args, **kwargs):
#         try:
#             user_lat = float(request.query_params.get('latitude'))
#             user_lon = float(request.query_params.get('longitude'))
#             service = request.query_params.get('service')

#             if not service:
#                 return Response({"error": "Service is required"}, status=status.HTTP_400_BAD_REQUEST)

#             # Fetch service providers offering the given service
#             service_providers = ServiceProvider.objects.filter(
#                 status='approved', is_approved=True
#             ).annotate(
#                 distance=F('latitude')  # Placeholder, will calculate distance manually
#             )

#             # Calculate distance for each provider
#             provider_data = []
#             for provider in service_providers:
#                 provider_distance = haversine(user_lat, user_lon, float(provider.latitude), float(provider.longitude))
#                 provider_data.append({
#                     "id": provider.id,
#                     "username": provider.username,
#                     "email": provider.email,
#                     "phone": provider.phone,
#                     "latitude": provider.latitude,
#                     "longitude": provider.longitude,
#                     "distance_km": round(provider_distance, 2),
#                     "image": provider.image.url if provider.image else None
#                 })

#             # Sort by nearest distance
#             provider_data = sorted(provider_data, key=lambda x: x["distance_km"])

#             return Response({
#                 "status": "success",
#                 "service_providers": provider_data
#             }, status=status.HTTP_200_OK)
        
#         except ValueError:
#             return Response({"error": "Invalid latitude or longitude"}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Service, ServiceProvider
class NearestServiceProviders(APIView):
    def haversine(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two geo-coordinates."""
        R = 6371  # Radius of Earth in km
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R * c  # Distance in km

    def get(self, request, *args, **kwargs):
        try:
            user_lat = float(request.query_params.get('latitude'))
            user_lon = float(request.query_params.get('longitude'))
            service_id = request.query_params.get('service')

            if not user_lat or not user_lon or not service_id:
                return Response({"error": "Latitude, longitude, and service ID are required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user_lat = float(user_lat)
                user_lon = float(user_lon)
                service_id = int(service_id)
            except ValueError:
                return Response({"error": "Invalid latitude, longitude, or service ID format"}, status=status.HTTP_400_BAD_REQUEST)

            # Get service providers linked to the requested service
            service_providers = ServiceProvider.objects.filter(
                id__in=Service.objects.filter(service=service_id).values_list('service_provider', flat=True),
                status='approved',
                is_approved=True
            )
            services = Service.objects.filter(service=service_id)
            if not services.exists():
                return Response({"error": "No services found with the given ID."}, status=status.HTTP_404_NOT_FOUND)

            # Calculate distance and filter providers within 50 km
            provider_data = []
            for provider in service_providers:
                provider_distance = self.haversine(user_lat, user_lon, float(provider.latitude), float(provider.longitude))
                
                if provider_distance <= 50:  # Only include providers within 50km
                    provider_data.append({
                        "id": provider.id,
                        "username": provider.username,
                        "email": provider.email,
                        "phone": provider.phone,
                        "latitude": provider.latitude,
                        "longitude": provider.longitude,
                        "distance_km": round(provider_distance, 2),
                        # "price": service.price,
                        "image": provider.image.url if provider.image else None
                    })

            # Sort by nearest distance
            provider_data = sorted(provider_data, key=lambda x: x["distance_km"])

            return Response({
                "status": "success",
                "service_providers": provider_data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class ServiceProviderAvailableSlots(APIView):
    def get(self, request, *args, **kwargs):
        try:
            provider_id = request.query_params.get('provider_id')
            date_str = request.query_params.get('date')

            if not provider_id or not date_str:
                return Response({"error": "Service Provider ID and date are required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                provider_id = int(provider_id)
                selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return Response({"error": "Invalid Service Provider ID or date format"}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch available slots
            available_slots = ServiceAvailableTime.objects.filter(
                service_provider_id=provider_id,
                date=selected_date,
                is_booked=False
            ).select_related("slot")

            if not available_slots.exists():
                return Response({"message": "No available slots for the selected date"}, status=status.HTTP_200_OK)

            serializer = ServiceAvailableTimeSerializer(available_slots, many=True)

            return Response({
                "status": "success",
                "available_slots": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class BookingViewSet(viewsets.ModelViewSet):
#     queryset = Booking.objects.all()
#     serializer_class = BookingSerializer
#     http_method_names = ['post']

#     def create(self, request, *args, **kwargs):
#         try:
#             # ✅ Get request data
#             user_id = request.data.get('user_id')
#             service_id = request.data.get('service_id')
#             service_provider_id = request.data.get('provider_id')
#             slot_id = request.data.get('slot_id')
#             date_str = request.data.get('date')  # Date in string format (YYYY-MM-DD)

#             # ✅ Validate required fields
#             if not all([user_id, service_id, service_provider_id, slot_id, date_str]):
#                 return Response(
#                     {"status": "failed", "message": "User, Service, Provider, Slot, and Date are required."},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             # ✅ Convert IDs to integers
#             user_id = int(user_id)
#             service_id = int(service_id)
#             service_provider_id = int(service_provider_id)
#             slot_id = int(slot_id)

#             # ✅ Convert date to date object
#             try:
#                 selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
#             except ValueError:
#                 return Response(
#                     {"status": "failed", "message": "Invalid date format. Use YYYY-MM-DD."},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             # ✅ Get User instance
#             user = User.objects.get(id=user_id)

#             # ✅ Get Service instance (corrected query)
#             service = Service.objects.get(service_id=service_id, service_provider_id=service_provider_id)

#             # ✅ Get Slot instance
#             slot = TimeSlot.objects.get(id=slot_id)

#             # ✅ Check slot availability for the selected date
#             available_slot = ServiceAvailableTime.objects.filter(
#                 service_provider_id=service_provider_id,
#                 slot_id=slot_id,
#                 date=selected_date,
#                 is_booked=False,
#             ).first()

#             if not available_slot:
#                 return Response(
#                     {"status": "failed", "message": "This slot is already booked or not available on the selected date."},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             # ✅ Check if the slot is already booked on the given date
#             if Booking.objects.filter(
#                 slot=slot,
#                 service_provider_id=service_provider_id,
#                 booking_date__date=selected_date,
#                 status__in=['booked', 'ongoing', 'paid'],
#             ).exists():
#                 return Response(
#                     {"status": "failed", "message": "This slot is already booked for the selected date."},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             # ✅ Combine date with slot start time
#             booking_datetime = datetime.combine(selected_date, slot.slot_start)

#             # ✅ Create a new booking with the selected date and slot
#             booking = Booking.objects.create(
#                 user=user,
#                 service=service,
#                 service_provider=service.service_provider,
#                 slot=slot,
#                 booking_date=booking_datetime,
#                 status="booked",
#             )

#             # ✅ Mark the slot as booked in ServiceAvailableTime
#             available_slot.is_booked = True
#             available_slot.save()

#             # ✅ Serialize and return the booking data
#             serializer = BookingSerializer(booking)
#             return Response(
#                 {
#                     "status": "success",
#                     "message": "Slot booked successfully.",
#                     "booking": serializer.data,
#                 },
#                 status=status.HTTP_201_CREATED,
#             )

#         except User.DoesNotExist:
#             return Response(
#                 {"status": "failed", "message": "User not found."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )
#         except Service.DoesNotExist:
#             return Response(
#                 {"status": "failed", "message": "Service not found."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )
#         except TimeSlot.DoesNotExist:
#             return Response(
#                 {"status": "failed", "message": "Time slot not found."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )
#         except ValueError:
#             return Response(
#                 {"status": "failed", "message": "Invalid ID format."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         except Exception as e:
#             return Response(
#                 {"status": "failed", "message": "An error occurred.", "error": str(e)},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )

# class BookingViewSet(viewsets.ModelViewSet):
#     queryset = Booking.objects.all()
#     serializer_class = BookingSerializer
#     http_method_names = ["post"]

#     def create(self, request, *args, **kwargs):
#         try:
#             # ✅ Get request data
#             user_id = request.data.get("user_id")
#             service_provider_id = request.data.get("provider_id")
#             slot_id = request.data.get("slot_id")
#             date_str = request.data.get("date")  # Date in string format (YYYY-MM-DD)

#             # ✅ Validate required fields (without service_id)
#             if not all([user_id, service_provider_id, slot_id, date_str]):
#                 return Response(
#                     {"status": "failed", "message": "User, Provider, Slot, and Date are required."},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             # ✅ Convert IDs to integers
#             user_id = int(user_id)
#             service_provider_id = int(service_provider_id)
#             slot_id = int(slot_id)

#             # ✅ Convert date to date object
#             try:
#                 selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
#             except ValueError:
#                 return Response(
#                     {"status": "failed", "message": "Invalid date format. Use YYYY-MM-DD."},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             # ✅ Get User instance
#             user = User.objects.get(id=user_id)

#             # ✅ Get Slot instance
#             slot = TimeSlot.objects.get(id=slot_id)

#             # ✅ Automatically fetch Service associated with the provider (optional handling if no service)
#             service = Service.objects.filter(service_provider_id=service_provider_id).first()
#             if not service:
#                 return Response(
#                     {"status": "failed", "message": "No service found for this provider."},
#                     status=status.HTTP_404_NOT_FOUND,
#                 )

#             # ✅ Check slot availability for the selected date
#             available_slot = ServiceAvailableTime.objects.filter(
#                 service_provider_id=service_provider_id,
#                 slot_id=slot_id,
#                 date=selected_date,
#                 is_booked=False,
#             ).first()

#             if not available_slot:
#                 return Response(
#                     {"status": "failed", "message": "This slot is already booked or not available on the selected date."},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             # ✅ Check if the slot is already booked on the given date
#             if Booking.objects.filter(
#                 slot=slot,
#                 service_provider_id=service_provider_id,
#                 booking_date__date=selected_date,
#                 status__in=["booked", "ongoing", "paid"],
#             ).exists():
#                 return Response(
#                     {"status": "failed", "message": "This slot is already booked for the selected date."},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             # ✅ Combine date with slot start time
#             booking_datetime = datetime.combine(selected_date, slot.slot_start)

#             # ✅ Create a new booking with the selected date and slot
#             booking = Booking.objects.create(
#                 user=user,
#                 service=service,
#                 service_provider=service.service_provider,
#                 slot=slot,
#                 booking_date=booking_datetime,
#                 status="booked",
#             )

#             # ✅ Mark the slot as booked in ServiceAvailableTime
#             available_slot.is_booked = True
#             available_slot.save()

#             # ✅ Serialize and return the booking data
#             serializer = BookingSerializer(booking)
#             return Response(
#                 {
#                     "status": "success",
#                     "message": "Slot booked successfully.",
#                     "booking": serializer.data,
#                 },
#                 status=status.HTTP_201_CREATED,
#             )

#         except User.DoesNotExist:
#             return Response(
#                 {"status": "failed", "message": "User not found."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )
#         except TimeSlot.DoesNotExist:
#             return Response(
#                 {"status": "failed", "message": "Time slot not found."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )
#         except ValueError:
#             return Response(
#                 {"status": "failed", "message": "Invalid ID format."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         except Exception as e:
#             return Response(
#                 {"status": "failed", "message": "An error occurred.", "error": str(e)},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )


from decimal import Decimal
from datetime import datetime

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        try:
            # ✅ Get request data
            user_id = request.data.get("user_id")
            service_provider_id = request.data.get("provider_id")
            slot_id = request.data.get("slot_id")
            date_str = request.data.get("date")  # Date in string format (YYYY-MM-DD)

            # ✅ Validate required fields (without service_id)
            if not all([user_id, service_provider_id, slot_id, date_str]):
                return Response(
                    {"status": "failed", "message": "User, Provider, Slot, and Date are required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # ✅ Convert IDs to integers
            user_id = int(user_id)
            service_provider_id = int(service_provider_id)
            slot_id = int(slot_id)

            # ✅ Convert date to date object
            try:
                selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return Response(
                    {"status": "failed", "message": "Invalid date format. Use YYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # ✅ Get User instance
            user = User.objects.get(id=user_id)

            # ✅ Get Slot instance
            slot = TimeSlot.objects.get(id=slot_id)

            # ✅ Automatically fetch Service associated with the provider
            service = Service.objects.filter(service_provider_id=service_provider_id).first()
            if not service:
                return Response(
                    {"status": "failed", "message": "No service found for this provider."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # ✅ Check slot availability for the selected date
            available_slot = ServiceAvailableTime.objects.filter(
                service_provider_id=service_provider_id,
                slot_id=slot_id,
                date=selected_date,
                is_booked=False,
            ).first()

            if not available_slot:
                return Response(
                    {"status": "failed", "message": "This slot is already booked or not available on the selected date."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # ✅ Check if the slot is already booked on the given date
            if Booking.objects.filter(
                slot=slot,
                service_provider_id=service_provider_id,
                booking_date__date=selected_date,
                status__in=["booked", "ongoing", "paid"],
            ).exists():
                return Response(
                    {"status": "failed", "message": "This slot is already booked for the selected date."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # ✅ Calculate platform fee (10% of service price)
            price = service.price
            platform_fee = round(Decimal(price) * Decimal(0.10), 2)  # 10% of service price

            # ✅ Combine date with slot start time
            booking_datetime = datetime.combine(selected_date, slot.slot_start)

            # ✅ Create a new booking with platform fee
            booking = Booking.objects.create(
                user=user,
                service=service,
                service_provider=service.service_provider,
                slot=slot,
                booking_date=booking_datetime,
                platform_fee=platform_fee,
                status="booked",
            )

            # ✅ Mark the slot as booked in ServiceAvailableTime
            available_slot.is_booked = True
            available_slot.save()

            # ✅ Serialize and return the booking data
            serializer = BookingSerializer(booking)
            return Response(
                {
                    "status": "success",
                    "message": "Slot booked successfully.",
                    "platform_fee": f"{platform_fee} INR",
                    "booking": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        except User.DoesNotExist:
            return Response(
                {"status": "failed", "message": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except TimeSlot.DoesNotExist:
            return Response(
                {"status": "failed", "message": "Time slot not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except ValueError:
            return Response(
                {"status": "failed", "message": "Invalid ID format."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"status": "failed", "message": "An error occurred.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            
# class UserBookingAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         try:
#             # ✅ Get user_id from query params
#             user_id = request.query_params.get("user_id")

#             # ✅ Validate user_id
#             if not user_id:
#                 return Response(
#                     {"status": "failed", "message": "User ID is required."},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             # ✅ Check if user exists
#             try:
#                 user = User.objects.get(id=user_id)
#             except User.DoesNotExist:
#                 return Response(
#                     {"status": "failed", "message": "User not found."},
#                     status=status.HTTP_404_NOT_FOUND,
#                 )

#             # ✅ Get booked and ongoing services for the user
#             booked_services = Booking.objects.filter(
#                 user_id=user_id, status="booked"
#             ).select_related("service", "user", "slot")

#             ongoing_services = Booking.objects.filter(
#                 user_id=user_id, status="ongoing"
#             ).select_related("service", "user", "slot")

#             # ✅ Serialize data
#             booked_serializer = UserBookingSerializer(booked_services, many=True)
#             ongoing_serializer = UserBookingSerializer(ongoing_services, many=True)

#             return Response(
#                 {
#                     "status": "success",
#                     "booked_services": booked_serializer.data,
#                     "ongoing_services": ongoing_serializer.data,
#                 },
#                 status=status.HTTP_200_OK,
#             )

#         except Exception as e:
#             return Response(
#                 {
#                     "status": "failed",
#                     "message": "An error occurred while fetching booking details.",
#                     "error": str(e),
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )

# class UserBookingAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         try:
#             # ✅ Get user_id from query params
#             user_id = request.query_params.get("user_id")

#             # ✅ Validate user_id
#             if not user_id:
#                 return Response(
#                     {"status": "failed", "message": "User ID is required."},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             # ✅ Check if user exists
#             try:
#                 user = User.objects.get(id=user_id)
#             except User.DoesNotExist:
#                 return Response(
#                     {"status": "failed", "message": "User not found."},
#                     status=status.HTTP_404_NOT_FOUND,
#                 )

#             # ✅ Get booked and ongoing services for the user
#             booked_services = Booking.objects.filter(
#                 user_id=user_id, status="booked"
#             ).select_related("service", "user", "slot")

#             ongoing_services = Booking.objects.filter(
#                 user_id=user_id, status="ongoing"
#             ).select_related("service", "user", "slot")

#             # ✅ Serialize data
#             booked_serializer = UserBookingSerializer(booked_services, many=True)
#             ongoing_serializer = UserBookingSerializer(ongoing_services, many=True)

#             # ✅ Convert price to string in the serialized data
#             booked_data = booked_serializer.data
#             ongoing_data = ongoing_serializer.data

#             for booking in booked_data:
#                 if "service_details" in booking:
#                     booking["service_details"]["price"] = str(
#                         booking["service_details"]["price"]
#                     )

#             for booking in ongoing_data:
#                 if "service_details" in booking:
#                     booking["service_details"]["price"] = str(
#                         booking["service_details"]["price"]
#                     )

#             # ✅ Return final response
#             return Response(
#                 {
#                     "status": "success",
#                     "booked_services": booked_data,
#                     "ongoing_services": ongoing_data,
#                 },
#                 status=status.HTTP_200_OK,
#             )

#         except Exception as e:
#             return Response(
#                 {
#                     "status": "failed",
#                     "message": "An error occurred while fetching booking details.",
#                     "error": str(e),
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )


class UserBookingAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # ✅ Get user_id from query params
            user_id = request.query_params.get("user_id")

            # ✅ Validate user_id
            if not user_id:
                return Response(
                    {"status": "failed", "message": "User ID is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # ✅ Check if user exists
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response(
                    {"status": "failed", "message": "User not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # ✅ Get booked and ongoing services for the user
            all_services = Booking.objects.filter(
                user_id=user_id, status__in=["booked", "ongoing","completed"]
            ).select_related("service", "user", "slot")

            # ✅ Serialize data
            serializer = UserBookingSerializer(all_services, many=True)
            all_data = serializer.data

            # ✅ Convert price to string and add status to the serialized data
            for booking in all_data:
                if "service_details" in booking:
                    booking["service_details"]["price"] = str(
                        booking["service_details"]["price"]
                    )
                booking_status = booking.get("status")
                booking["status"] = booking_status  # Keep the status as is for reference

            # ✅ Return final response
            # return Response(
            #     {
            #         "status": "success",
            #         "all_services": all_data,
            #     },
            #     status=status.HTTP_200_OK,
            # )
            return Response(all_data,status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {
                    "status": "failed",
                    "message": "An error occurred while fetching booking details.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

            
            
class UserMarkNotArrivedAPIView(APIView):
    def patch(self, request, *args, **kwargs):
        try:
            # ✅ Get booking_id from request data
            booking_id = request.data.get("booking_id")

            # ✅ Validate booking_id
            if not booking_id:
                return Response(
                    {"status": "failed", "message": "Booking ID is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # ✅ Check if the booking exists
            try:
                booking = Booking.objects.get(id=booking_id)
            except Booking.DoesNotExist:
                return Response(
                    {"status": "failed", "message": "Booking not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # ✅ Check if the current status is 'booked'
            if booking.status != "booked":
                return Response(
                    {"status": "failed", "message": "Only 'booked' bookings can be marked as 'not arrived'."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # ✅ Update status to 'not arrived'
            booking.status = "not arrived"
            booking.save()

            # ✅ Serialize updated data
            serializer = BookingSerializer(booking)
            return Response(
                {
                    "status": "success",
                    "message": "Booking status changed to 'not arrived'.",
                    "booking": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"status": "failed", "message": "An error occurred while updating booking status.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            
class UserMarkCompletedAPIView(APIView):
    def patch(self, request, *args, **kwargs):
        try:
            # ✅ Get booking_id from request data
            booking_id = request.data.get("booking_id")

            # ✅ Validate booking_id
            if not booking_id:
                return Response(
                    {"status": "failed", "message": "Booking ID is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # ✅ Check if the booking exists
            try:
                booking = Booking.objects.get(id=booking_id)
            except Booking.DoesNotExist:
                return Response(
                    {"status": "failed", "message": "Booking not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # ✅ Check if the current status is 'ongoing'
            if booking.status != "ongoing":
                return Response(
                    {"status": "failed", "message": "Only 'ongoing' bookings can be marked as 'completed'."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # ✅ Update status to 'completed'
            booking.status = "completed"
            booking.save()

            # ✅ Serialize updated data
            serializer = BookingSerializer(booking)
            return Response(
                {
                    "status": "success",
                    "message": "Booking status changed to 'completed'.",
                    "booking": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"status": "failed", "message": "An error occurred while updating booking status.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            
            
class UserBookingHistoryAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # ✅ Get user_id from query params
            user_id = request.query_params.get("user_id")

            # ✅ Validate user_id
            if not user_id:
                return Response(
                    {"status": "failed", "message": "User ID is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # ✅ Check if user exists
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response(
                    {"status": "failed", "message": "User not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # ✅ Get only paid and not arrived services for the user
            paid_and_not_arrived_services = Booking.objects.filter(
                user_id=user_id, status__in=["paid", "not arrived"]
            ).select_related("service", "slot")

            # ✅ Serialize these services
            booking_serializer = UserBookingSerializer(
                paid_and_not_arrived_services, many=True
            )

            return Response(
                booking_serializer.data,  # ✅ Show both paid and not arrived services
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"status": "failed", "message": "An error occurred.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

# class UserBookingHistoryAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         try:
#             # ✅ Get user_id from query params
#             user_id = request.query_params.get("user_id")

#             # ✅ Validate user_id
#             if not user_id:
#                 return Response(
#                     {"status": "failed", "message": "User ID is required."},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             # ✅ Check if user exists
#             try:
#                 user = User.objects.get(id=user_id)
#             except User.DoesNotExist:
#                 return Response(
#                     {"status": "failed", "message": "User not found."},
#                     status=status.HTTP_404_NOT_FOUND,
#                 )

#             # ✅ Get user's bookings with the required statuses
#             not_arrived_services = Booking.objects.filter(
#                 user_id=user_id, status="not arrived"
#             ).select_related("service", "slot")

#             completed_services = Booking.objects.filter(
#                 user_id=user_id, status="completed"
#             ).select_related("service", "slot")

#             paid_services = Booking.objects.filter(
#                 user_id=user_id, status="paid"
#             ).select_related("service", "slot")

#             # ✅ Serialize data
#             not_arrived_serializer = UserBookingSerializer(not_arrived_services, many=True)
#             completed_serializer = UserBookingSerializer(completed_services, many=True)
#             paid_serializer = UserBookingSerializer(paid_services, many=True)

#             return Response(
#                 {
#                     "status": "success",
#                     "not_arrived_services": not_arrived_serializer.data,
#                     "completed_services": completed_serializer.data,
#                     "paid_services": paid_serializer.data,
#                 },
#                 status=status.HTTP_200_OK,
#             )

#         except Exception as e:
#             return Response(
#                 {"status": "failed", "message": "An error occurred while fetching booking history.", "error": str(e)},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )

# class UpiPaymentView(viewsets.ModelViewSet):
#     serializer_class = UpiPaymentSerializer
#     http_method_names = ['post']

#     def create(self, request, *args, **kwargs):
#         """Create a UPI Payment Entry for a Booking and Update Status"""
#         booking_id = request.data.get("booking_id")
#         upi_id = request.data.get("upi_id")

#         if not booking_id or not upi_id:
#             return Response(
#                 {"message": "Booking ID and UPI ID are required"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Check if the booking exists
#         booking = get_object_or_404(Booking, id=booking_id)

#         # Check if a payment already exists for this booking
#         if Upi.objects.filter(booking=booking).exists():
#             return Response(
#                 {"message": "Payment already exists for this booking"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         try:
#             # Create a new UPI Payment entry
#             upi_payment = Upi.objects.create(
#                 booking=booking,
#                 upi_id=upi_id,
#                 status="success"  # Initially, mark payment as successful
#             )

#             # Update booking status to "paid" after payment creation
#             booking.status = "paid"
#             booking.save()

#             serializer = UpiPaymentSerializer(upi_payment)
#             return Response(
#                 {"message": "UPI Payment Successful, Booking Status Updated", "data": serializer.data},
#                 status=status.HTTP_201_CREATED
#             )
#         except Exception as e:
#             return Response(
#                 {"message": "An error occurred", "error": str(e)},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

class UpiPaymentView(viewsets.ModelViewSet):
    serializer_class = UpiPaymentSerializer
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        """Create a UPI Payment Entry for a Booking and Update Status"""
        booking_id = request.data.get("booking_id")
        upi_id = request.data.get("upi_id")

        if not booking_id or not upi_id:
            return Response(
                {"message": "Booking ID and UPI ID are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ✅ Check if the booking exists
        booking = get_object_or_404(Booking, id=booking_id)

        # ✅ Check if a payment already exists for this booking
        if Upi.objects.filter(booking=booking).exists():
            return Response(
                {"message": "Payment already exists for this booking"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # ✅ Calculate total amount (Service Price + Platform Fee)
            service_price = booking.service.price
            platform_fee = booking.platform_fee
            total_amount = service_price + platform_fee

            # ✅ Create a new UPI Payment entry with total amount
            upi_payment = Upi.objects.create(
                booking=booking,
                upi_id=upi_id,
                amount=total_amount,  # ✅ Store total amount in UPI
                status="success",  # Mark payment as successful initially
            )

            # ✅ Update booking status to "paid" after payment creation
            booking.status = "paid"
            booking.save()

            serializer = UpiPaymentSerializer(upi_payment)
            return Response(
                {
                    "message": "UPI Payment Successful, Booking Status Updated",
                    "total_amount": f"{total_amount} INR",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"message": "An error occurred", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# class CardPaymentView(viewsets.ModelViewSet):
#     serializer_class = CardSerializer
#     http_method_names = ['post']

#     def create(self, request, *args, **kwargs):
#         """Create a Card Payment Entry for a Booking and Update Status"""
#         booking_id = request.data.get("booking_id")
#         card_holder_name = request.data.get("card_holder_name")
#         card_number = request.data.get("card_number")
#         expiry_date = request.data.get("expiry_date")
#         cvv = request.data.get("cvv")

#         # Validate required fields
#         if not all([booking_id, card_holder_name, card_number, expiry_date, cvv]):
#             return Response(
#                 {"message": "All fields (Booking ID, Card Holder Name, Card Number, Expiry Date, CVV) are required"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         try:
#             booking = Booking.objects.get(id=booking_id)

#             # Check if a payment already exists for this booking
#             if Card.objects.filter(booking=booking).exists():
#                 return Response(
#                     {"message": "Payment already exists for this booking"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             # Create a new Card Payment entry
#             card_payment = Card.objects.create(
#                 booking=booking,
#                 card_holder_name=card_holder_name,
#                 card_number=card_number,
#                 expiry_date=expiry_date,
#                 cvv=cvv,
#                 status="success"  # Assuming success for now
#             )

#             # Update booking status to "paid"
#             booking.status = "paid"
#             booking.save()

#             serializer = CardSerializer(card_payment)
#             return Response(
#                 {"message": "Card Payment Successful, Booking Status Updated", "data": serializer.data},
#                 status=status.HTTP_201_CREATED
#             )

#         except Booking.DoesNotExist:
#             return Response(
#                 {"message": "Booking not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

class CardPaymentView(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        """Create a Card Payment Entry for a Booking and Update Status"""
        booking_id = request.data.get("booking_id")
        card_holder_name = request.data.get("card_holder_name")
        card_number = request.data.get("card_number")
        expiry_date = request.data.get("expiry_date")
        cvv = request.data.get("cvv")

        # ✅ Validate required fields
        if not all([booking_id, card_holder_name, card_number, expiry_date, cvv]):
            return Response(
                {
                    "message": "All fields (Booking ID, Card Holder Name, Card Number, Expiry Date, CVV) are required"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # ✅ Check if the booking exists
            booking = Booking.objects.get(id=booking_id)

            # ✅ Check if a payment already exists for this booking
            if Card.objects.filter(booking=booking).exists():
                return Response(
                    {"message": "Payment already exists for this booking"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # ✅ Calculate total amount (Service Price + Platform Fee)
            service_price = booking.service.price
            platform_fee = booking.platform_fee
            total_amount = service_price + platform_fee

            # ✅ Create a new Card Payment entry with total amount
            card_payment = Card.objects.create(
                booking=booking,
                card_holder_name=card_holder_name,
                card_number=card_number,
                expiry_date=expiry_date,
                cvv=cvv,
                amount=total_amount,  # ✅ Store total amount in Card payment
                status="success",  # Assuming success for now
            )

            # ✅ Update booking status to "paid"
            booking.status = "paid"
            booking.save()

            serializer = CardSerializer(card_payment)
            return Response(
                {
                    "message": "Card Payment Successful, Booking Status Updated",
                    "total_amount": f"{total_amount} INR",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        except Booking.DoesNotExist:
            return Response(
                {"message": "Booking not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"message": "An error occurred", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
