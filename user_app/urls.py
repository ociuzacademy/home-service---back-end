from django.urls import path

from django.contrib import admin
from.import views
from django.urls import path, re_path,include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import *
from rest_framework.routers import DefaultRouter


schema_view = get_schema_view(
    openapi.Info(
        title="Home Service API",
        default_version="v1",
        description="API documentation for the Home Service system.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@homeservice.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],

)

router = DefaultRouter()
router.register(r"user_registration",UserRegistrationView)
router.register(r'view_services_by_category', ServiceByCategoryView, basename='view_services_by_category')
# router.register(r'customer_support', CustomerSupportView, basename='customer_support')
# router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'reviews', CreateReviewView, basename='review')
router.register(r'service-providers', ServiceProviderViewSet, basename="service-provider")
router.register(r'book_slot', BookingViewSet, basename='book_slot')
router.register(r'upi_payment', UpiPaymentView, basename='upi_payment')
router.register(r'card_payment', CardPaymentView, basename='card_payment')
router.register(r'favorite-service-providers', FavoriteServiceProviderViewSet, basename='favorite-service-provider')
router.register(r'view_favorite-service-providers', ViewFavoriteServiceProviderViewSet, basename='view_favorite-service-provider')  

urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),

    path("",include(router.urls)),
    path('login/',LoginView.as_view(),name='login'),
    path('update_profile/', UpdateProfileview.as_view(), name='update_Profile'),
    # path('view_services/',ViewServicesView.as_view({'get':'list'}),name='view_services'),
    path('view_category/',ViewCategoryView.as_view({'get':'list'}),name='view_category'),
    path('view_user_profile/',ViewUserProfileView.as_view({'get':'list'}),name='view_user_profile'),
    path('browse_services/',BrowseServicesView.as_view({'get':'list'}),name='browse_services'),
    path('available_slots/', ServiceProviderAvailableSlots.as_view(), name='available_slots'),
    path('booking_history/', BookingHistoryViewSet.as_view({'get':'list'}), name='booking_history'),
    path('nearest-service-providers/', NearestServiceProviders.as_view(), name='nearest_service_providers'),
    path('view_bookings/', UserBookingAPIView.as_view(), name='view_bookings'),
    path("user_booking_history/", UserBookingHistoryAPIView.as_view(), name="user_booking_history"),
    path("status_not_arrived/", UserMarkNotArrivedAPIView.as_view(), name="status_not_arrived"),
    path("status_completed/", UserMarkCompletedAPIView.as_view(), name="status_completed"),
    path("remove_favorite-service-providers/", RemoveFavoriteServiceProviderView.as_view(), name="remove_favorite-service-providers"),
     
]









