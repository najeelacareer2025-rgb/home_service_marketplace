from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('customer', 'Customer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)  
    icon = models.ImageField(upload_to='category_icons/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    provider = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="services",null=True,
    blank=True)
    img = models.ImageField(upload_to='service_images/', blank=True, null=True)
    rating = models.FloatField(default=4.0)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name





class Booking(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.customer.username} - {self.service.name}"


class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment for booking {self.booking.id}"



class Offering(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    featured = models.BooleanField(default=False)
    provider_name = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Appointment(models.Model):
    customer_name = models.CharField(max_length=100)
    offering = models.ForeignKey(Offering, on_delete=models.CASCADE, related_name="appointments")
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.customer_name} - {self.offering.title} on {self.date} at {self.time}"
