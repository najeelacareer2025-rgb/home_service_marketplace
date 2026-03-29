from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model

from .models import Service, Booking
from .forms import CustomerSignupForm, StaffSignupForm
from .forms import StaffRegisterForm
User = get_user_model()





from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from django.urls import reverse

from .models import Service, Booking
from .forms import CustomerSignupForm, StaffSignupForm

User = get_user_model()


def is_admin(user):
    return user.is_staff or user.is_superuser or user.role == 'admin'


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    services = Service.objects.all()
    bookings = Booking.objects.all()
    staff_users = User.objects.filter(is_staff=True)
    my_bookings = Booking.objects.filter(service__provider=request.user)

    context = {
        'services': services,
        'bookings': bookings,
        'my_bookings': my_bookings,
        'staff_users': staff_users,
        'total_users': User.objects.count(),
        'total_services': services.count(),
        'total_bookings': bookings.count(),
    }
    return render(request, 'marketplace/admin_dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def bookings(request):
    """Admin view: show all bookings"""
    bookings = Booking.objects.all()
    return render(request, 'marketplace/bookings.html', {'bookings': bookings})


@login_required
@user_passes_test(is_admin)
def update_booking_status(request, booking_id):
    """Admin view: update booking status"""
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status:
            booking.status = new_status
            booking.save()
            messages.success(request, f"Booking status updated to {new_status}!")
        return redirect('bookings')
    return render(request, 'marketplace/update_booking.html', {'booking': booking})


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        role = request.POST.get('role')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.role = role
            user.save()
            messages.success(request, "Registration successful! Click below to login.")
            return redirect('login')

    return render(request, 'marketplace/register.html')


class RoleBasedLoginView(LoginView):
    template_name = 'marketplace/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.role == 'admin' or user.is_superuser:
            return reverse('admin_dashboard')
        elif user.role == 'staff'or user.is_staff:
            return reverse('staff_dashboard')
        else:
            return reverse('customer_dashboard')
    def form_invalid(self, form):
         messages.error(self.request, "Invalid username or password. Please try again.")
         return super().form_invalid(form)

def role_required(role):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.role != role:
                return HttpResponseForbidden("You are not authorized to view this page.")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator






@login_required
def edit_staff(request, staff_id):
    staff = get_object_or_404(User, id=staff_id, is_staff=True)
    if request.method == 'POST':
        staff.username = request.POST.get('username', staff.username)
        staff.email = request.POST.get('email', staff.email)
        staff.save()
        messages.success(request, "Staff updated successfully!")
        return redirect('admin_dashboard')
    return render(request, 'marketplace/edit_staff.html', {'staff': staff})

@login_required
def delete_staff(request, staff_id):
    staff = get_object_or_404(User, id=staff_id, is_staff=True)
    if request.method == 'POST':
        staff.delete()
        messages.success(request, "Staff deleted successfully!")
        return redirect('admin_dashboard')
    return render(request, 'marketplace/confirm_delete_staff.html', {'staff': staff})


@login_required
def edit_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        service.name = request.POST.get('name', service.name)
        service.price = request.POST.get('price', service.price)

        provider_id = request.POST.get('provider')
        if provider_id:  # must be numeric
            service.provider = get_object_or_404(User, id=provider_id)

        service.save()
        messages.success(request, "Service updated successfully!")
        return redirect('admin_dashboard')

    return render(request, 'marketplace/edit_service.html', {
        'service': service,
        'staff_users': User.objects.filter(is_staff=True)
    })

@login_required
def bookings(request):
    my_bookings = Booking.objects.filter(service__provider=request.user)
    return render(request, 'marketplace/bookings.html', {'my_bookings': my_bookings})


@login_required
def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        service.delete()
        messages.success(request, "Service deleted successfully!")
        return redirect('admin_dashboard')
    return render(request, 'marketplace/confirm_delete_service.html', {'service': service})
@login_required
def service_overview(request):
    services = Service.objects.all()
    return render(request, "marketplace/service_overview.html", {"services": services})
@login_required
def all_bookings(request):
    bookings = Booking.objects.all().order_by('-date')
    return render(request, 'marketplace/all_bookings.html', {'bookings': bookings})

@login_required
def create_service(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        provider_id = request.POST.get('provider')

        if provider_id and provider_id.isdigit():
            provider = get_object_or_404(User, id=int(provider_id))
        else:
            provider = None  

        Service.objects.create(
            name=name,
            price=price,
            provider=provider
        )
        messages.success(request, "Service created successfully!")
        return redirect('admin_dashboard')

    staff_users = User.objects.filter(is_staff=True)
    return render(request, 'marketplace/create_service.html', {'staff_users': staff_users})


@login_required
def booking_detail(request):
    my_bookings = Booking.objects.filter(service__provider=request.user)
    return render(request, 'marketplace/bookings.html', {'my_bookings': my_bookings})
from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking

def update_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == "POST":
       
        new_status = request.POST.get("status")
        if new_status:
            booking.status = new_status
            booking.save()
            return redirect("admin_dashboard")  

    return render(request, "marketplace/update_booking.html", {"booking": booking})


@login_required
def staff_dashboard(request):
    services = Service.objects.filter(provider=request.user)
    bookings = Booking.objects.filter(service__provider=request.user)

    context = {
        'services': services,
        'bookings': bookings,
    }
    return render(request, 'marketplace/staff_dashboard.html', context)


@login_required
def staff_update_booking_status(request, booking_id, status):
    booking = get_object_or_404(Booking, id=booking_id, service__provider=request.user)
    booking.status = status
    booking.save()
    messages.success(request, f"Booking status updated to {status}!")
    return redirect('staff_dashboard')

@login_required
def customer_dashboard(request):
    bookings = Booking.objects.filter(customer=request.user)
    services = Service.objects.all()

    context = {
        'bookings': bookings,
        'services': services,
    }
    return render(request, 'marketplace/customer_dashboard.html', context)



@login_required
def book_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        Booking.objects.create(
            customer=request.user,
            service=service,
            date=request.POST.get('date'),
            status='Pending'
        )
       
        messages.success(request, f"You have successfully booked {service.name}!")
        return redirect('customer_dashboard')

    return render(request, 'marketplace/book_service.html', {'service': service})



@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    booking.status = 'Cancelled'
    booking.save()
    messages.success(request, "Your booking has been cancelled.")
    return redirect('customer_dashboard')





from .models import Service

def home(request):
    services = Service.objects.all()
    featured_services = Service.objects.filter(featured=True)[:6]  # only featured
    return render(request, 'marketplace/home.html', {
        'services': services,
        'featured_services': featured_services
    })
def featured_services(request):
    featured_services = Service.objects.filter(featured=True)
    return render(request, "marketplace/featured_services.html", {
        "featured_services": featured_services,
    })




def about(request):
    return render(request, 'marketplace/about.html')

def contact(request):
    return render(request, 'marketplace/contact.html')



@login_required
def bookings(request):
    return render(request, 'marketplace/bookings.html')
@login_required
def profile(request):
    return render(request, 'marketplace/profile.html')

@login_required
def user_profile(request):
    return render(request, 'marketplace/user_profile.html', {'user': request.user})

def service_list(request):
    services = Service.objects.all()
    return render(request, 'marketplace/service_list.html', {'services': services})

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'marketplace/service_detail.html', {'service': service})

@login_required
def book_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        booking = Booking.objects.create(
            customer=request.user,
            service=service,
            date=request.POST['date']
        )
        return redirect('booking_detail', pk=booking.pk)
    return render(request, 'marketplace/book_service.html', {'service': service})

@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'marketplace/booking_detail.html', {'booking': booking})



def logout_view(request):
    logout(request)
    return redirect('home')

def categories(request):
    category_list = [
        {"name": "Plumber", "icon": "bi-tools"},
        {"name": "Smart Home", "icon": "bi-house-door"},
        {"name": "Carpenter", "icon": "bi-hammer"},
        {"name": "Pest Control", "icon": "bi-bug"},
        {"name": "Painter", "icon": "bi-brush"},
        {"name": "Corporate", "icon": "bi-building"},
        {"name": "AC Repair", "icon": "bi-snow"},
        {"name": "Salon", "icon": "bi-scissors"},
        {"name": "Security", "icon": "bi-shield-lock"},
    ]
    return render(request, 'marketplace/categories.html', {"categories": category_list})


def customer_register(request):
    if request.method == 'POST':
        form = CustomerSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer registered successfully!")
            return redirect('login')
    else:
        form = CustomerSignupForm()
    return render(request, 'marketplace/customer_register.html', {'form': form})


@login_required
def staff_register(request):
    if request.method == 'POST':
        form = StaffSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff registered successfully!")
            return redirect('admin_dashboard')
    else:
        form = StaffSignupForm()
    return render(request, 'marketplace/staff_register.html', {'form': form})


from .models import Category, Service

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'marketplace/category_list.html', {'categories': categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    services = category.services.all()
    return render(request, 'marketplace/category_detail.html', {
        'category': category,
        
    })



def category_list(request):
    categories = Category.objects.all()
    return render(request, "marketplace/category_list.html", {"categories": categories})

from .models import Service

from django.db.models import Q

def service_list(request):
    query = request.GET.get('q')
    if query:
        services = Service.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(provider__username__icontains=query)
        )
    else:
        services = Service.objects.all()

    featured_services = Service.objects.filter(featured=True)[:3]

    return render(request, 'marketplace/service_list.html', {
        'services': services,
        'featured_services': featured_services,
    })

from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking

def make_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

   
    return redirect("payment_success")

def payment_success(request):
    context = {
        "transaction_id": "DEMO123456", 
        "message": "Payment successfully completed."
    }
    return render(request, "marketplace/payment_success.html", context)


from .forms import ProfileForm



@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('user_profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'marketplace/edit_profile.html', {'form': form})

import os
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from huggingface_hub import InferenceClient
from .models import Service
from dotenv import load_dotenv

# Load environment variables from .env in project root
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Hugging Face setup
HF_API_TOKEN = os.getenv("HF_TOKEN")   # safely loaded from .env
HF_MODEL = "meta-llama/Llama-3.2-1B-Instruct"

client = InferenceClient(model=HF_MODEL, token=HF_API_TOKEN)


@csrf_exempt
def chat_page(request):
    if "chat_history" not in request.session:
        request.session["chat_history"] = []

    if request.method == "POST":
        user_message = request.POST.get("message", "").strip()
        if user_message:
            # Save user message
            request.session["chat_history"].append({"sender": "user", "text": user_message})

            # Build context from your Service model
            services = Service.objects.all()
            context = "\n".join([f"{s.name}: {s.description}" for s in services])

            # Construct system + user messages
            messages = [
                {"role": "system", "content": f"You are an assistant for Urban Home Services. Available services:\n{context}\nAnswer based only on the services above."},
                {"role": "user", "content": user_message},
            ]

            try:
                # Hugging Face chat completion call
                response_obj = client.chat_completion(
                    model=HF_MODEL,
                    messages=messages,
                    max_tokens=300,
                    stream=False,
                )

                # Extract reply text
                ai_reply = response_obj.choices[0].message.content

            except Exception as e:
                ai_reply = f"Error: {str(e)}"

            # Save AI reply
            request.session["chat_history"].append({"sender": "ai", "text": ai_reply})
            request.session.modified = True

    return render(request, "marketplace/chat.html", {"chat_history": request.session["chat_history"]})
