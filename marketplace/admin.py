from django.contrib import admin

# Register your models here.

from .models import Service, Booking, Payment

# marketplace/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Offering, Appointment

class CustomUserAdmin(UserAdmin):
    # Show role in the list view
    list_display = ('username', 'email', 'profile_pic', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('username',)

    # Add role to the user form
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)



from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "provider", "price", "featured")  
    list_filter = ("featured", "provider")  
    search_fields = ("name", "provider__username")



@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'service', 'date', 'status')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'timestamp', 'success')



@admin.register(Offering)
class OfferingAdmin(admin.ModelAdmin):
    list_display = ("title", "provider_name", "featured")
    list_filter = ("featured", "provider_name")
    search_fields = ("title", "provider_name")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "offering", "date", "time")
    list_filter = ("date", "offering")
    search_fields = ("customer_name", "offering__title")
