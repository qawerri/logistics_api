from django.db import models
from django.conf import settings


class Driver(models.Model):
    """Водитель логистической компании."""
    name = models.CharField(max_length=255)
    license_number = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=20)
    experience_years = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.license_number})"


class Vehicle(models.Model):
    """Транспортное средство."""
    VEHICLE_TYPES = [
        ('truck', 'Грузовик'),
        ('van', 'Фургон'),
        ('lorry', 'Фура'),
        ('courier', 'Курьер'),
    ]
    STATUS_CHOICES = [
        ('available', 'Свободен'),
        ('on_route', 'В рейсе'),
        ('maintenance', 'На обслуживании'),
    ]

    plate_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    capacity_kg = models.IntegerField(help_text="Грузоподъёмность в кг")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    driver = models.ForeignKey(
        Driver, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='vehicles'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_vehicle_type_display()} {self.plate_number}"


class Order(models.Model):
    """Заказ на перевозку."""
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('assigned', 'Назначен'),
        ('in_transit', 'В пути'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]

    pickup_address = models.CharField(max_length=500)
    delivery_address = models.CharField(max_length=500)
    cargo_description = models.TextField()
    weight_kg = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    vehicle = models.ForeignKey(
        Vehicle, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='orders'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Заказ #{self.id}: {self.pickup_address} → {self.delivery_address}"


class TrackingEvent(models.Model):
    """Событие отслеживания заказа."""
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='tracking_events'
    )
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='tracking_events'
    )

    def __str__(self):
        return f"Событие #{self.id} для заказа #{self.order_id}"