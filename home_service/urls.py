"""
URL configuration for home_service project.
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from marketplace import views
from marketplace.views import RoleBasedLoginView
from marketplace.views import chat_page

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', RoleBasedLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboards
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('customer-dashboard/', views.customer_dashboard, name='customer_dashboard'),

    # Bookings (Admin only)
    path('bookings/', views.bookings, name='bookings'),
    path('bookings/<int:booking_id>/update/', views.update_booking_status, name='update_booking_status'),
    

    # Staff management
    path('staff/register/', views.staff_register, name='staff_register'),
    path('staff/<int:staff_id>/edit/', views.edit_staff, name='edit_staff'),
    path('staff/<int:staff_id>/delete/', views.delete_staff, name='delete_staff'),
    path('staff/booking/<int:booking_id>/status/<str:status>/', views.staff_update_booking_status, name='staff_update_booking_status'),

    # Services management
    path('services/', views.service_list, name='services'),
   
    path('featured-services/', views.featured_services, name='featured_services'),


    path('services/create/', views.create_service, name='create_service'),
    path('services/<int:service_id>/edit/', views.edit_service, name='edit_service'),
    path('services/<int:service_id>/delete/', views.delete_service, name='delete_service'),
    path('services/<int:pk>/', views.service_detail, name='service_detail'),
    path('services/<int:pk>/book/', views.book_service, name='book_service'),
    path('update-booking/<int:booking_id>/', views.update_booking, name='update_booking'),
    path('serviceoverview/', views.service_overview, name='serviceoverview'),
    path('all_bookings/', views.all_bookings, name= 'all_bookings'),

    # Customer bookings
    path('booking/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('bookings/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('payment/<int:booking_id>/', views.make_payment, name='make_payment'),
    path("payment-success/", views.payment_success, name="payment_success"),


    # General pages
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('categories/', views.category_list, name='categories'),
    path('categories/<slug:slug>/', views.category_detail, name='category_detail'),
    path("chat/", chat_page, name="chat_page"), 

    # Profiles
    path('profile/', views.profile, name='profile'),
    path('user-profile/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
