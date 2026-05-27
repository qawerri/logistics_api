from rest_framework import serializers
from .models import Driver, Vehicle, Order, TrackingEvent


class DriverSerializer(serializers.ModelSerializer):
    """Сериализатор для водителя."""
    class Meta:
        model = Driver
        fields = [
            'id', 'name', 'license_number', 'phone',
            'experience_years', 'rating', 'is_active'
        ]
        read_only_fields = ['id']


class VehicleSerializer(serializers.ModelSerializer):
    """
    Сериализатор для транспортного средства.
    При чтении отдаёт вложенного водителя, при записи — только driver_id.
    """
    driver = DriverSerializer(read_only=True)
    driver_id = serializers.PrimaryKeyRelatedField(
        queryset=Driver.objects.filter(is_active=True),
        source='driver',
        write_only=True,
        required=False
    )

    class Meta:
        model = Vehicle
        fields = [
            'id', 'plate_number', 'vehicle_type', 'capacity_kg',
            'status', 'driver', 'driver_id', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class TrackingEventSerializer(serializers.ModelSerializer):
    """Сериализатор для события отслеживания."""
    order = serializers.StringRelatedField(read_only=True)
    order_id = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(),
        source='order',
        write_only=True
    )
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TrackingEvent
        fields = ['id', 'order', 'order_id', 'description', 'location', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для заказа.
    При чтении отдаёт вложенное ТС, при записи — только vehicle_id.
    """
    vehicle = VehicleSerializer(read_only=True)
    vehicle_id = serializers.PrimaryKeyRelatedField(
    queryset=Vehicle.objects.filter(status='available'),
        source='vehicle',
        write_only=True,
        required=False
    )
    tracking_events = TrackingEventSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'pickup_address', 'delivery_address', 'cargo_description',
            'weight_kg', 'status', 'vehicle', 'vehicle_id',
            'tracking_events', 'created_at', 'delivered_at'
        ]
        read_only_fields = ['id', 'created_at', 'tracking_events']