from django.urls import path
from.import views
from .views import *

urlpatterns = [
    path('',views.login,name='login'),
    path('admin_index/',views.admin_index,name='admin_index'),
    path('add_service/',views.add_service,name='add_service'),
    path('view_services',views.view_services,name='view_services'),
    # path('view_service_providers', views.view_service_providers, name='view_service_providers'),
    path('approve_service_provider', views.approve_service_provider, name='approve_service_provider'),
    path('reject_service_provider', views.reject_service_provider, name='reject_service_provider'),
    # path('edit_services', views.edit_services, name='edit_services'),
    # path('delete_sevices', views.delete_sevices, name='delete_sevices'),
    path('add_category', views.add_category, name='add_category'),
    path('category-list/', category_list, name='category_list'),
    path('bookings/', admin_booking_list, name='bookings'),
    path('view_approved_providers/', views.approved_providers, name='view_approved_providers'),
    path('view_rejected_providers/', views.rejected_providers, name='view_rejected_providers'),
    path('manage_providers/', views.manage_service_providers, name='manage_service_providers'),
    path('view_provider_services/', views.view_provider_services, name='view_provider_services'),
    path('edit_service/', views.edit_service, name='edit_service'),
    path("delete_service/", views.delete_service, name="delete_service"),
    path("report_analysis/", views.admin_report, name="report_analysis"),
    path("view_users/", views.view_users, name="view_users"),

]