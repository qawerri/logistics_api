from django.contrib import admin
from .models import Driver, Vehicle, Order, TrackingEvent


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    """Администрирование водителей."""
    list_display = ['id', 'name', 'license_number', 'phone', 'experience_years', 'rating', 'is_active']
    list_filter = ['is_active', 'experience_years']
    search_fields = ['name', 'license_number', 'phone']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    """Администрирование транспортных средств."""
    list_display = ['id', 'plate_number', 'vehicle_type', 'capacity_kg', 'status', 'driver']
    list_filter = ['vehicle_type', 'status']
    search_fields = ['plate_number']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Администрирование заказов."""
    list_display = ['id', 'pickup_address', 'delivery_address', 'weight_kg', 'status', 'vehicle', 'created_at']
    list_filter = ['status', 'vehicle', 'created_at']
    search_fields = ['pickup_address', 'delivery_address', 'cargo_description']
    readonly_fields = ['created_at']


@admin.register(TrackingEvent)
class TrackingEventAdmin(admin.ModelAdmin):
    """Администрирование событий отслеживания."""
    list_display = ['id', 'order', 'description', 'location', 'created_at', 'user']
    list_filter = ['created_at']
    search_fields = ['description', 'location']
    readonly_fields = ['created_at', 'user']
