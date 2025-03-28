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
router.register(r"service_registration",ServiceProviderRegisterView)
router.register(r'add_services', AddServicesView,basename='add_services')
router.register(r'view_services', ViewServicesView, basename='view_services')
# router.register(r'serviceprovider_availability', ServiceAvailableTimeViewSet, basename='serviceprovider_availability')
# router.register(r'confirm_booking', ConfirmBookingViewSet, basename='confirm_booking')
# router.register(r'cancel_booking', CancelBookingViewSet, basename='cancel_booking')
# router.register(r'complete_booking', CompleteBookingViewSet, basename='complete_booking')
router.register(r'service_available_time',SetAvailableSlotsView,basename='service_available_time')


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
    # path('admin/', admin.site.urls),
    path('login/',LoginView.as_view(),name='login'),
    # path('update_service/', UpdateServiceView.as_view(), name='update_service'),
    path('update_profile/', UpdateProfileview.as_view(), name='update_Profile'),
    # path('delete_service/', DeleteServiceView.as_view(), name='delete_service'),
    path('view_categories/',CategoryView.as_view({'get':'list'}),name='view_categories'),
    path('view_service_provider_profile/', ViewServiceProviderProfileView.as_view({'get': 'list'}), name='view_service_provider_profile'),
    path('provider_view_reviews/', ProviderBookingReviewsAPIView.as_view(),name='provider_view_reviews'),
    # path('view_added_service/', ServiceView.as_view({'get': 'list'}),name='view_added_service'),
    path('view_provider_services/', ServiceView.as_view({'get': 'provider_services'}), name='view_provider_services'),
    path('view_slots/',ServiceProviderSlotsView.as_view({'get':'list'}),name='view_slots'),
    path('view_bookings/', ServiceProviderBookingAPIView.as_view(), name='view_bookings'),
    path('provider_booking_history/', ServiceProviderBookingHistoryAPIView.as_view(), name='provider_booking_history'),
    path("single_booking/", SingleBookingAPIView.as_view(), name="single_booking"),
    path("status_ongoing/", OngoingBookingStatusAPIView.as_view(), name="status_ongoing"),
    path("service_provider_15days/", ServiceProviderWorkSummaryAPIView.as_view(), name="service_provider_15days"),
    path("last_10_works/", ServiceProviderLast10WorksAPIView.as_view(), name="last_10_works"),
    path("service_provider_earnings/", ServiceProviderEarningsAPIView.as_view(), name="service_provider_earnings"),
]

