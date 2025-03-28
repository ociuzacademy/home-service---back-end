from arrow import now
from django.shortcuts import get_object_or_404, render,redirect
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.response import Response
from rest_framework import status,viewsets,generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from admin_app.models import *
from user_app.models import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from datetime import datetime, timedelta

# Create your views here.

class ServiceProviderRegisterView(viewsets.ModelViewSet):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer
    http_method_names = ['post']
    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            response_data = {
                "status": "success",
                "message": "Service Provider Registration successful",
                "data": serializer.data  # This will show the saved user data
            }
            return Response(response_data,status=status.HTTP_201_CREATED)
        else:
            response_data = {
                "status": "failed",
                "message": "Invalid Details",
                "errors": serializer.errors,  # Optionally show validation errors
                "data": request.data  # This will show the data that was sent
            }
            return Response(response_data,status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            email = request.data.get('email')
            password = request.data.get('password')

            try:
                service = ServiceProvider.objects.get(email=email)
                # ⚠️ This is insecure (plaintext password check); it's better to use Django's `check_password()` if passwords are hashed.
                if password == service.password:
                    response_data = {
                        "status": "success",
                        "message": "User logged in successfully",
                        "user_id": service.id,
                        "username": str(service.username),
                        "userstatus": str(service.status),
                        "data": request.data  # Show the sent data
                    }
                    request.session['id'] = service.id
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "status": "failed",
                        "message": "Invalid credentials",
                        "data": request.data  # Show the sent data
                    }, status=status.HTTP_401_UNAUTHORIZED)

            except ServiceProvider.DoesNotExist:
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


class CategoryServiceListView(viewsets.ReadOnlyModelViewSet):
    serializer_class = ViewServiceSerializer

    def get_queryset(self):
        category_id = self.request.query_params.get('category_id')  # Get category_id from URL params
        if category_id:
            return TblService.objects.filter(id=category_id)
        return TblService.objects.all()  # Return all categories if no category_id is provided

# class AddServicesView(viewsets.ViewSet):  # Use ViewSet if you want custom bulk handling
#     def create(self, request, *args, **kwargs):
#         try:
#             services_data = request.data  # This expects a **list of objects**
#             print(services_data)
#             if not isinstance(services_data, list):
#                 return Response({"error": "Expected a list of services"}, status=status.HTTP_400_BAD_REQUEST)

#             serializer = ServiceSerializer(data=services_data, many=True)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()

#             # After saving all services, update the service provider status.
#             # Assuming all services belong to the same provider (you can change this logic if needed).
#             service_provider_id = services_data[0].get('service_provider')
#             service_provider = ServiceProvider.objects.get(id=service_provider_id)
#             service_provider.status = 'services_added'
#             service_provider.save()

#             return Response(
#                 {"message": "Services added successfully", "data": serializer.data},
#                 status=status.HTTP_201_CREATED
#             )

#         except Exception as e:
#             print("Error in AddServicesView:", e)
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CategoryView(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = categorySerializer

    def  list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
        
# class ServiceAvailableTimeCreateView(viewsets.GenericViewSet):
#     def post(self, request, args, *kwargs):
#         service_provider_id = request.data.get('service_provider')
#         # Check if service_provider_id is provided
#         if not service_provider_id:
#             return Response({"error": "Service Provider ID is required."}, status=status.HTTP_400_BAD_REQUEST)
#         # Validate the Service Provider exists
#         service_provider = ServiceProvider.objects.filter(id=service_provider_id).first()
#         if not service_provider:
#             return Response({"error": "Invalid Service Provider."}, status=status.HTTP_404_NOT_FOUND)
#         # Serialize and save availability
#         serializer = ServiceAvailableTimeSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 service_provider_available_time = serializer.save(service_provider=service_provider)
#                 service_provider_available_time.create_slots()  # Generate slots
#                 return Response({"success": "Availability added successfully."}, status=status.HTTP_200_OK)
#             except Exception as e:
#                 return Response({"error": f"Failed to create slots: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# def create_slots(self, slot_duration=30):
#         """
#         Create slots for the available time.
#         """
#         start_time = datetime.combine(self.date, self.start_time)
#         end_time = datetime.combine(self.date, self.end_time)
#         slot_duration = timedelta(minutes=slot_duration)

#         slots = []
#         while start_time + slot_duration <= end_time:
#             # Calculate the end time for the slot
#             slot_end_time = start_time + slot_duration

#             slots.append(Slots(
#                 doctor_available_time=self,
#                 date=self.date,  # Use the availability date for the slot
#                 start_time=start_time.time(),  # Store the start time as time object
#                 end_time=slot_end_time.time(),  # Store the end time as time object
#                 status="available"  # Default status for the slot
#             ))

#             start_time += slot_duration

#         # Bulk create the slots
#         Slots.objects.bulk_create(slots)  # Save all slots at once

# def save(self, args, *kwargs):
#     """
#     Override save to generate slots after saving DoctorAvailableTime.
#     """
#     super().save(*args, **kwargs)
#     if not self.slots.exists():  # Ensure slots are not duplicated
#         self.create_slots()


class ViewServicesView(viewsets.ReadOnlyModelViewSet):
    queryset = TblService.objects.all()
    serializer_class = ViewServiceSerializer

    def list(self, request, *args, **kwargs):
        category_id = request.query_params.get("category_id")  # Get category_id from params

        if category_id:
            services = self.queryset.filter(category_id=category_id)  # Filter services by category
            if services.exists():
                serializer = self.get_serializer(services, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "No services found for this category."}, status=status.HTTP_404_NOT_FOUND)
        else:
            # No filtering, return all services
            return super().list(request, *args, **kwargs)
        

class UpdateServiceView(generics.UpdateAPIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    http_method_names=['patch']
    def update(self, request, *args, **kwargs):
        # Retrieve the service_id from the request data
        service_id = request.data.get('service_id')
        if not service_id:
            return Response({"detail": "Service ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the service instance using the provided service_id
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            return Response({"detail": "Service not found."}, status=status.HTTP_404_NOT_FOUND)

        # Update the Service instance with the provided data
        serializer = self.get_serializer(service, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({"detail": "Service updated successfully.", "service": serializer.data}, status=status.HTTP_200_OK)

class DeleteServiceView(generics.DestroyAPIView):
    queryset = Service.objects.all()

    def delete(self, request, *args, **kwargs):
        # Retrieve the service_id from the request data
        service_id = request.data.get('service_id')
        if not service_id:
            return Response({"detail": "Service ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the service instance using the provided service_id
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            return Response({"detail": "Service not found."}, status=status.HTTP_404_NOT_FOUND)

        # Delete the service instance
        service.delete()

        return Response({"detail": "Service deleted successfully."}, status=status.HTTP_200_OK)


class UpdateProfileview(generics.UpdateAPIView):
    serializer_class=ServiceProviderSerializer
    queryset=ServiceProvider.objects.all()
    http_method_names=['patch']

    def update(self, request, *args, **kwargs):
        service_provider_id= request.data.get('id')
        if not service_provider_id:
            return Response({"detail": "Service Provider ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the service instance using the provided service_id
            service_provider = ServiceProvider.objects.get(id=service_provider_id)
        except Service.DoesNotExist:
            return Response({"detail": "Service Provider not found."}, status=status.HTTP_404_NOT_FOUND)

        # Update the Service instance with the provided data
        serializer = self.get_serializer(service_provider, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({"detail": "Profile updated successfully.", "service": serializer.data}, status=status.HTTP_200_OK)              


from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import ServiceProvider, ServiceAvailableTime
from .serializers import *

class ServiceProviderSlotsView(viewsets.ReadOnlyModelViewSet):
    serializer_class = TimeSlotSerializer
    queryset = TimeSlot.objects.all()
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        provider_id = request.query_params.get('id')

        if not provider_id:
            return Response({"error": "Missing 'id' query parameter"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            service_provider = ServiceProvider.objects.get(id=provider_id)
        except ServiceProvider.DoesNotExist:
            return Response({"error": "Service Provider not found"}, status=status.HTTP_404_NOT_FOUND)

        slots = TimeSlot.objects.filter(service_provider=service_provider).order_by('slot_start')
        serializer = self.get_serializer(slots, many=True)

        return Response({
            # "id": service_provider.id,
            # "email": service_provider.email,
            # "image": service_provider.image.url if service_provider.image else None,
            # "status": service_provider.status,
            "slots": serializer.data
        }, status=status.HTTP_200_OK)

# class ServiceAvailableTimeViewSet(viewsets.GenericViewSet):
#     serializer_class = ServiceAvailableTimeSerializer
#     queryset = ServiceAvailableTime.objects.all()

#     def create(self, request, *args, **kwargs):
#         service_provider_id = request.data.get('service_provider_id')
#         if not service_provider_id:
#             return Response(
#                 {"error": "Service Provider ID is required."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
            
#         service_provider = get_object_or_404(ServiceProvider, id=service_provider_id)
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 service_available_time = serializer.save(service_provider=service_provider)
#                 service_available_time.create_slots()
#                 return Response(
#                     {"success": "Availability added successfully."},
#                     status=status.HTTP_200_OK
#                 )
#             except Exception as e:
#                 return Response(
#                     {"error": f"Failed to create slots: {str(e)}"},
#                     status=status.HTTP_500_INTERNAL_SERVER_ERROR
#                 )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ConfirmBookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = StatusBookingSerializer
    http_method_names = ['patch']

    def patch(self, request, *args, **kwargs):
        booking_id = request.data.get("booking_id")
        try:
            booking = Booking.objects.get(id=booking_id)  # Retrieve the Employee object
        except Booking.DoesNotExist:
            return Response(
                {"status": "failed", "message": "Repair request not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        data = request.data.copy()
        data['status'] =  "confirmed"

        # Perform partial update with the provided data
        serializer = StatusBookingSerializer(booking, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Booking Confirmed successfully",
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "status": "failed",
                    "message": "Invalid Details",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
)
            
# class CancelBookingViewSet(viewsets.ModelViewSet):
#     queryset = Bookings.objects.all()
#     serializer_class = StatusBookingSerializer
#     http_method_names = ['patch']

#     def patch(self, request):
#         booking_id = request.data.get("booking_id")

#         if not booking_id:
#             return Response({"error": "Booking ID is required"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             booking = Bookings.objects.get(id=booking_id, status="pending")

#             # Update booking status
#             booking.status = "cancelled"
#             booking.save()

#             # Update slot status to available
#             slot = Slots.objects.get(id=booking.slot_id)
#             slot.status = "available"
#             slot.save()

#             return Response({"message": "Booking cancelled successfully"}, status=status.HTTP_200_OK)

#         except Bookings.DoesNotExist:
#             return Response({"error": "No pending booking found with this ID"}, status=status.HTTP_404_NOT_FOUND)

#         except Slots.DoesNotExist:
#             return Response({"error": "Slot not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
# class CompleteBookingViewSet(viewsets.ModelViewSet):
#     queryset = Booking.objects.all()
#     serializer_class = StatusBookingSerializer
#     http_method_names = ['patch']

#     def patch(self, request, *args, **kwargs):
#         booking_id = request.data.get("booking_id")
#         try:
#             booking = Booking.objects.get(id=booking_id, status="confirmed")  # Retrieve the Employee object
#         except Booking.DoesNotExist:
#             return Response(
#                 {"status": "failed", "message": "Repair request not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         data = request.data.copy()
#         data['status'] =  "completed"

#         # Perform partial update with the provided data
#         serializer = StatusBookingSerializer(booking, data=data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {
#                     "status": "success",
#                     "message": "Booking completed successfully",
#                 },
#                 status=status.HTTP_200_OK
#             )
#         else:
#             return Response(
#                 {
#                     "status": "failed",
#                     "message": "Invalid Details",
#                     "errors": serializer.errors,
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
# )
            
            
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

class ServiceView(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    http_method_names = ['get']

    @action(detail=False, methods=['get'], url_path='provider-services')
    def provider_services(self, request):
        service_provider_id = request.query_params.get('id')

        if not service_provider_id:
            return Response({'error': 'Provider ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            service_provider = ServiceProvider.objects.get(id=service_provider_id)
        except ServiceProvider.DoesNotExist:
            return Response({'error': 'Service provider not found'}, status=status.HTTP_404_NOT_FOUND)

        services = Service.objects.filter(service_provider=service_provider)
        serializer = ServiceSerializer(services, many=True)

        if services.exists():
            # Get the category from the first service (assuming all have the same category)
            category = services.first().category
            category_data = CategorySerializer(category).data
        else:
            category_data = None  # No services found, category data is empty

        response_data = {
            "category": category_data,
            "services": serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)

            
            
class ViewServiceProviderProfileView(viewsets.ReadOnlyModelViewSet):
    queryset = ServiceProvider.objects.all()
    serializer_class = ViewServiceProviderSerializer

    def list(self, request, *args, **kwargs):
        service_provider_id = request.query_params.get("id")  # Get user id from query parameters

        if service_provider_id:
            try:
                service_provider = self.queryset.get(id=service_provider_id)
                serializer = self.get_serializer(service_provider)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ServiceProvider.DoesNotExist:
                return Response({"detail": "Service Provider not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            # No user_id provided, return all users (if required)
            return super().list(request, *args, **kwargs)
        
class ProviderBookingReviewsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # ✅ Get provider_id from query params
            provider_id = request.query_params.get("provider_id")

            # ✅ Validate provider_id
            if not provider_id:
                return Response(
                    {"status": "failed", "message": "Provider ID is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # ✅ Check if the provider exists
            try:
                provider = ServiceProvider.objects.get(id=provider_id)
            except ServiceProvider.DoesNotExist:
                return Response(
                    {"status": "failed", "message": "Service Provider not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # ✅ Get all reviews related to the provider's bookings
            reviews = Review.objects.filter(
                booking__service_provider_id=provider_id
            ).select_related("booking__service", "booking__user")

            # ✅ Check if reviews exist
            if not reviews.exists():
                return Response(
                    [],
                    status=status.HTTP_200_OK,
                )

            # ✅ Serialize review data
            serializer = ReviewSerializer(reviews, many=True)
            return Response(
                
                    # "status": "success",
                    # "message": "Reviews retrieved successfully.",
                    serializer.data,
              
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {
                    "status": "failed",
                    "message": "An error occurred while fetching reviews.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    

# class AddServicesView(viewsets.ViewSet):
#     def create(self, request, *args, **kwargs):
#         """Create multiple Service Entries for a Service Provider"""
#         try:
#             serializer = AddServicesSerializer(data=request.data)
#             serializer.is_valid(raise_exception=True)

#             category = serializer.validated_data['category']
#             service_provider = serializer.validated_data['service_provider']
#             services_data = serializer.validated_data['services']

#             service_provider_obj = ServiceProvider.objects.get(id=service_provider.id)
#             service_provider.status = "services_added"  # Update status
#             service_provider.save()

#             created_services = []
#             for service_data in services_data:
#                 service = service_data['service']  # TblService instance
#                 price = service_data['price']

#                 service_obj = Service.objects.create(
#                     category=category,
#                     service_provider=service_provider,
#                     service=service,  
#                     price=price
#                 )
#                 created_services.append({"service": service.id, "price": price})

#             return Response({
#                 "category": category.id,
#                 "service_provider": service_provider.id,
#                 "services": created_services
#             }, status=status.HTTP_201_CREATED)

#         except Exception as e:
#             print("Error in AddServicesView:", e)
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddServicesView(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        """Create multiple Service Entries for a Service Provider"""
        try:
            serializer = AddServicesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            category = serializer.validated_data['category']
            service_provider = serializer.validated_data['service_provider']
            services_data = serializer.validated_data['services']

            service_provider_obj = ServiceProvider.objects.get(id=service_provider.id)
            service_provider_obj.status = "services_added"  # Update status
            service_provider_obj.save()

            created_services = []
            for service_data in services_data:
                service = service_data['service']  # Should be a valid TblService instance
                price = service_data['price']

                service_obj = Service.objects.create(
                    category=category,
                    service_provider=service_provider,
                    service=service,  
                    price=price
                )
                created_services.append({"service": service.id, "price": float(price)})

            return Response({
                "category": category.id,  # Renamed to "categories"
                "service_provider": service_provider.id,
                "services": created_services
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print("Error in AddServicesView:", e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SetAvailableSlotsView(viewsets.ViewSet):
    """Allows service providers to select available slots for different dates"""

    def create(self, request):
        service_provider_id = request.data.get("service_provider_id")
        date = request.data.get("date")
        slot_ids = request.data.get("slots")  # List of slot IDs to set as available

        if not service_provider_id or not date or not slot_ids:
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            service_provider = ServiceProvider.objects.get(id=service_provider_id)
        except ServiceProvider.DoesNotExist:
            return Response({"error": "Service provider not found"}, status=status.HTTP_404_NOT_FOUND)

        # Delete previous availability records for the same date to prevent duplicates
        ServiceAvailableTime.objects.filter(
            service_provider=service_provider, date=date
        ).delete()

        # Create new availability records using serializer
        new_slots = []
        for slot_id in slot_ids:
            try:
                slot = TimeSlot.objects.get(id=slot_id)
                serializer = ServiceAvailableTimeSerializer(data={
                    "service_provider": service_provider.id,
                    "date": date,
                    "slot": slot.id,
                    "is_available": True
                })
                if serializer.is_valid():
                    serializer.save()
                    new_slots.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except TimeSlot.DoesNotExist:
                return Response({"error": f"Slot ID {slot_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Available slots updated successfully!", "slots": new_slots}, status=status.HTTP_200_OK)

class ServiceProviderBookingAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # ✅ Get provider_id from query params
            provider_id = request.query_params.get("provider_id")

            # ✅ Validate provider_id
            if not provider_id:
                return Response(
                    {"status": "failed", "message": "Provider ID is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # ✅ Check if provider exists
            try:
                provider = ServiceProvider.objects.get(id=provider_id)
            except ServiceProvider.DoesNotExist:
                return Response(
                    {"status": "failed", "message": "Service Provider not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # ✅ Get booked and ongoing services
            booked_services = Booking.objects.filter(
                service_provider_id=provider_id, status="booked"
            ).select_related("service", "user", "slot")

            ongoing_services = Booking.objects.filter(
                service_provider_id=provider_id, status="ongoing"
            ).select_related("service", "user", "slot")

            # ✅ Serialize data
            booked_serializer = BookingSerializer(booked_services, many=True)
            ongoing_serializer = BookingSerializer(ongoing_services, many=True)

            return Response(
                {
                    "booked_services": booked_serializer.data,
                    "ongoing_services": ongoing_serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"status": "failed", "message": "An error occurred.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            
class SingleBookingAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # ✅ Get booking_id from query params
            booking_id = request.query_params.get("booking_id")

            # ✅ Validate booking_id
            if not booking_id:
                return Response(
                    {"status": "failed", "message": "Booking ID is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # ✅ Get the booking instance
            try:
                booking = Booking.objects.select_related(
                    "service__category", "user", "slot"
                ).get(id=booking_id)
            except Booking.DoesNotExist:
                return Response(
                    {"status": "failed", "message": "Booking not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # ✅ Serialize the booking data
            serializer = SingleBookingSerializer(booking)

            # ✅ Return the booking details
            return Response(serializer.data,
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"status": "failed", "message": "An error occurred.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

            

class OngoingBookingStatusAPIView(APIView):
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

            # ✅ Get the booking and check if it exists
            try:
                booking = Booking.objects.get(id=booking_id)
            except Booking.DoesNotExist:
                return Response(
                    {"status": "failed", "message": "Booking not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # ✅ Check if the status is currently 'booked'
            if booking.status != "booked":
                return Response(
                    {"status": "failed", "message": "Only booked services can be updated to ongoing."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # ✅ Update the status to 'ongoing'
            booking.status = "ongoing"
            booking.save()

            # ✅ Return updated data
            serializer = BookingSerializer(booking)
            return Response(
                {"status": "success", "message": "Booking status updated to ongoing.", "data": serializer.data},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {
                    "status": "failed",
                    "message": "An error occurred while updating booking status.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            
class ServiceProviderBookingHistoryAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # ✅ Get provider_id from query params
            provider_id = request.query_params.get("provider_id")

            # ✅ Validate provider_id
            if not provider_id:
                return Response(
                    {"status": "failed", "message": "Provider ID is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # ✅ Convert provider_id to integer
            try:
                provider_id = int(provider_id)
            except ValueError:
                return Response(
                    {"status": "failed", "message": "Invalid Provider ID format."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # ✅ Check if provider exists
            try:
                provider = ServiceProvider.objects.get(id=provider_id)
            except ServiceProvider.DoesNotExist:
                return Response(
                    {"status": "failed", "message": "Service Provider not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # ✅ Get booking history (filtering 'not arrived', 'paid', and 'completed')
            booking_history = Booking.objects.filter(
                service_provider_id=provider_id,
                status__in=["not arrived", "completed","paid"],
            ).select_related("service", "user", "slot")

            # ✅ Check if any history exists
            if not booking_history.exists():
                return Response(
                    [],
                    status=status.HTTP_200_OK,
                )

            # ✅ Serialize data
            serializer = BookingSerializer(booking_history, many=True)
            return Response(
                
                    # "status": "success",
                    # "message": "Booking history retrieved successfully.",
                     serializer.data,
                
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"status": "failed", "message": "An error occurred.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            
            
            
from django.db.models import Sum
from django.db.models.functions import Cast
from django.db.models import Sum, DateField

class ServiceProviderWorkSummaryAPIView(APIView):
    def get(self, request, *args, **kwargs):
        """Fetch date and total amount for work done by provider with status 'paid' in the last 15 days."""
        service_provider_id = request.query_params.get("provider_id")

        if not service_provider_id:
            return Response(
                {"error": "Service Provider ID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get current date and calculate the date 15 days ago
        end_date = now().date()
        start_date = end_date - timedelta(days=15)

        # Fetch work done with 'paid' status in the last 15 days
        bookings = (
            Booking.objects.filter(
                service_provider_id=service_provider_id,
                status="paid",
                booking_date__date__range=[start_date, end_date],
            )
            .annotate(booking_date_casted=Cast("booking_date", DateField()))
            .values("booking_date_casted")
            .annotate(total_amount=Sum("service__price"))
            .order_by("-booking_date_casted")
        )

        if not bookings.exists():
            return Response(
                [],
                status=status.HTTP_200_OK,
            )

        # Return serialized data
        # return Response(
        #     {"status": "success", "work_summary": list(bookings)},
        #     status=status.HTTP_200_OK,
        # )
        return Response(list(bookings), status=status.HTTP_200_OK)
    
    
    
class ServiceProviderLast10WorksAPIView(APIView):
    def get(self, request, *args, **kwargs):
        """Fetch last 10 works done by the provider with service name, date, and amount."""
        service_provider_id = request.query_params.get("provider_id")

        if not service_provider_id:
            return Response(
                {"error": "Service Provider ID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Fetch last 10 works with 'paid' status, ordered by booking_date
        bookings = (
            Booking.objects.filter(
                service_provider_id=service_provider_id,
                status="paid"
            )
            .annotate(booking_date_casted=Cast("booking_date", DateField()))
            .values(
                "booking_date_casted",
                "service__service__service_name"  # ✅ Fetch service name
            )
            .annotate(total_amount=Sum("service__price"))
            .order_by("-booking_date_casted")[:10]  # ✅ Get only the last 10 works
        )

        if not bookings.exists():
            return Response([], status=status.HTTP_200_OK)

        # ✅ Prepare response data with service name, date, and total amount
        data = [
            {
                "service_name": booking["service__service__service_name"],
                "booking_date": booking["booking_date_casted"],
                "total_amount": booking["total_amount"],
            }
            for booking in bookings
        ]

        return Response(data, status=status.HTTP_200_OK)
    
    
class ServiceProviderEarningsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        provider_id = request.query_params.get("provider_id")

        # Validate provider_id
        if not provider_id:
            return Response(
                {"error": "Service Provider ID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Get service provider
            provider = ServiceProvider.objects.get(id=provider_id)

            # Filter completed and paid bookings
            completed_bookings = Booking.objects.filter(
                service_provider=provider,
                status__in=["paid",]
            )

            # Calculate total earnings
            total_earnings = completed_bookings.aggregate(total_earnings=Sum("service__price"))["total_earnings"] or 0.00

            return Response(
                {
                    "status": "success",
                    "service_provider": provider.username,
                    "total_earnings": float(total_earnings),
                },
                status=status.HTTP_200_OK,
            )

        except ServiceProvider.DoesNotExist:
            return Response(
                {"error": "Service Provider not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
