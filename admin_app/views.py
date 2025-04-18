from django.shortcuts import render
from django.shortcuts import get_object_or_404, render,redirect
from django.db.models import Sum
from .models import *
from django.contrib import messages
from service_app.models import *
from user_app.models import *
from django.core.paginator import Paginator
# Create your views here.

def admin_index(request):
    return render(request,'admin_index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            admin = Admin.objects.get(username=username,password=password)
            request.session['admin_id'] = admin.id
            return redirect('admin_index')
        except Admin.DoesNotExist:
            return redirect('login')

    return render(request, 'login.html')

# def login(request):
#     if request.method =='POST':
#         username=request.POST.get('username')
#         password=request.POST.get('password')

#         if username=='admin' and password=='admin':
#             return redirect('admin_index')
#     return render(request,'login.html')

def view_services(request):
    categories = Category.objects.all()
    category_id = request.GET.get("category")  # Get selected category from URL
    services = TblService.objects.filter(category_id=category_id) if category_id else TblService.objects.all()

    return render(request, "view_services.html", {"categories": categories, "services": services})



def view_service_providers(request):
    service_providers = ServiceProvider.objects.all()
    return render(request, 'view_service_providers.html', {'service_providers': service_providers})

# def approve_service_provider(request):
#     service_id = request.GET.get('id')
#     if service_id:
#         service = ServiceProvider.objects.get(id=service_id)
#         service.is_approved = True
#         service.status = "approved"
#         service.save()
#         messages.success(request, f"ServiceProvider {service.username} has been successfully approved!")
#     else:
#         messages.error(request, "Invalid service provider ID.")
#     return redirect('view_service_providers')

def manage_service_providers(request):
    # Filter providers with multiple statuses
    service_providers = ServiceProvider.objects.filter(
        status__in=["pending", "services_added","services_not_added"]
    )
    return render(request, "manage_service_providers.html", {"service_providers": service_providers})

def approved_providers(request):
    service_providers = ServiceProvider.objects.filter(status="approved")
    return render(request, "approved_providers.html", {"service_providers": service_providers})


def approve_service_provider(request):
    provider_id = request.GET.get("id")
    provider = get_object_or_404(ServiceProvider, id=provider_id)

    if provider.status != "services_added":
        messages.warning(request, "Cannot approve. Services have not been added yet.")
        return redirect("manage_service_providers")

    provider.status = "approved"
    provider.is_approved = True
    provider.save()
    
    messages.success(request, "Service provider approved successfully!")
    return redirect("manage_service_providers")

# def reject_service_provider(request):
#     service_id = request.GET.get('id')
#     if service_id:
#         service = ServiceProvider.objects.get(id=service_id)
#         service.is_approved = False
#         service.status = "rejected"
#         service.save()
#         messages.success(request, f"ServiceProvider {service.username} has been successfully rejected.")
#     else:
#         messages.error(request, "Invalid service provider ID.")
#     return redirect('view_service_providers')

def rejected_providers(request):
    service_providers = ServiceProvider.objects.filter(status="rejected")
    return render(request, "rejected_providers.html", {"service_providers": service_providers})

def reject_service_provider(request):
    provider_id = request.GET.get("id")
    provider = get_object_or_404(ServiceProvider, id=provider_id)

    if provider.status == "rejected":
        messages.warning(request, "Provider is already rejected.")
        return redirect("manage_service_providers")

    provider.status = "rejected"
    provider.is_approved = False  # just to be safe
    provider.save()

    if request.GET.get("from") == "approved":
        messages.error(request, "Approved service provider has been rejected.")
        return redirect("view_approved_providers")

    messages.error(request, "Service provider rejected successfully!")
    return redirect("manage_service_providers")

# def edit_services(request):
#     service_id=request.GET.get('id')
#     service=Services.objects.filter(id=service_id).first()

#     if request.method == "POST":
#         image = request.FILES.get("image")
#         name = request.POST.get("name")
#         sub_services_str = request.POST.get("sub_service")

#         # Split the sub-services string into a list
#         sub_service_list = [sub_service.strip() for sub_service in sub_services_str.split(",")]

#         # Update the service object
#         service.image = image if image else service.image  # Update image if provided
#         service.name = name
#         service.sub_service = sub_service_list
#         service.save()

#         messages.success(request, "Service updated successfully!")
#         return redirect("view_services")  # Redirect to the home page or another appropriate page

#     # Pass the service object to the template for display
#     context = {"service": service}
#     return render(request, "edit_services.html", context)

# def delete_sevices(request):
#     service_id=request.GET.get('id')
#     service=Services.objects.filter(id=service_id).first()
#     service.delete()
#     return redirect('view_services')

def add_service(request):
    if request.method == "POST":
        category_id = request.POST.get("category")
        service_name = request.POST.get("service_name")

        category = Category.objects.get(id=category_id)
        TblService.objects.create(category=category, service_name=service_name)

        return redirect("add_service")  # Redirect back to the form after submission

    categories = Category.objects.all()
    return render(request, "add_service.html", {"categories": categories})

def add_category(request):
    if request.method == "POST":
        category_name = request.POST.get("category")
        if category_name:
            Category.objects.create(category=category_name)
            return redirect('add_category')
    return render(request, "add_category.html")



def admin_booking_list(request):
     # Fetch all paid bookings
    paid_bookings = Booking.objects.filter(status="paid").select_related(
        "user", "service_provider", "service__service", "slot"
    )
    
    # Calculate total platform fee collected by admin
    total_platform_fee = paid_bookings.aggregate(total_fee=Sum("platform_fee"))["total_fee"] or 0.00

    return render(
        request,
        "bookings.html",
        {"bookings": paid_bookings, "total_platform_fee": total_platform_fee},
    )

def view_services_by_category(request):
    categories = Category.objects.all()
    category_id = request.GET.get("category")  # Get selected category from URL
    services = TblService.objects.filter(category_id=category_id) if category_id else TblService.objects.all()

    return render(request, "view_services.html", {"categories": categories, "services": services})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})


def view_provider_services(request):
    provider_id=request.GET.get('id')
    provider = get_object_or_404(ServiceProvider, id=provider_id)
    services = Service.objects.filter(service_provider=provider)

    return render(request, "view_provider_services.html", {
        "provider": provider,
        "services": services
    })
    
    
def edit_service(request):
    service_id = request.GET.get('id')
    service = get_object_or_404(TblService, id=service_id)
    categories = Category.objects.all()

    if request.method == "POST":
        category_id = request.POST.get("category")
        service_name = request.POST.get("service_name")

        # Update the service
        service.category_id = category_id
        service.service_name = service_name
        service.save()

        return redirect("view_services")

    return render(request, "edit_services.html", {"service": service, "categories": categories})


def delete_service(request):
    service_id=request.GET.get('id')
    service = get_object_or_404(TblService, id=service_id)
    service.delete()
    messages.success(request, "Service deleted successfully!")
    return redirect("view_services")


from django.shortcuts import render
from django.db.models import Count, Sum

def admin_report(request):
    # ✅ Total users and providers
    total_users = User.objects.count()
    total_providers = ServiceProvider.objects.count()

    # ✅ Booking status breakdown
    booking_stats = {
        "total_bookings": Booking.objects.count(),
        "booked": Booking.objects.filter(status="booked").count(),
        "paid": Booking.objects.filter(status="paid").count(),
        "ongoing": Booking.objects.filter(status="ongoing").count(),
        "not_arrived": Booking.objects.filter(status="not arrived").count(),
        "completed": Booking.objects.filter(status="completed").count(),
    }

    # ✅ Provider approval breakdown
    provider_stats = {
        "pending": ServiceProvider.objects.filter(status="pending").count(),
        "approved": ServiceProvider.objects.filter(status="approved").count(),
        "rejected": ServiceProvider.objects.filter(status="rejected").count(),
    }

    context = {
        "total_users": total_users,
        "total_providers": total_providers,
        "booking_stats": booking_stats,
        "provider_stats": provider_stats,
    }

    return render(request, "admin_report_analysis.html", context)


def view_users(request):
    users = User.objects.all()
    return render(request, "view_users.html", {"users": users})
