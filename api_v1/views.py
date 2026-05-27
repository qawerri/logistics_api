from django.utils.decorators import method_decorator
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework_extensions.cache.decorators import cache_response

from .models import Driver, Vehicle, Order, TrackingEvent
from .serializers import (
    DriverSerializer, VehicleSerializer, 
    OrderSerializer, TrackingEventSerializer
)
from .permissions import IsDriverOrReadOnly


class DriverViewSet(viewsets.ModelViewSet):
    """
    Представление для работы с водителями.
    
    Поддерживает CRUD, массовые операции, фильтрацию по имени и номеру прав.
    GET-запросы кешируются на 15 минут.
    """
    serializer_class = DriverSerializer
    queryset = Driver.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        name = self.request.query_params.get('name')
        license_number = self.request.query_params.get('license_number')
        is_active = self.request.query_params.get('is_active')
        
        if name:
            qs = qs.filter(name__icontains=name)
        if license_number:
            qs = qs.filter(license_number__icontains=license_number)
        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() == 'true')
        return qs

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @cache_response(60 * 15)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        if many:
            instances = [Driver.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        if many:
            instances = [Driver.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, partial=True, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        ids = request.query_params.get('ids')
        if ids:
            ids_list = [int(pk) for pk in ids.split(',')]
            Driver.objects.filter(pk__in=ids_list).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)


class VehicleViewSet(viewsets.ModelViewSet):
    """
    Представление для работы с транспортными средствами.
    
    Фильтрация по типу ТС, статусу, водителю и госномеру.
    """
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        vehicle_type = self.request.query_params.get('vehicle_type')
        status_filter = self.request.query_params.get('status')
        driver_id = self.request.query_params.get('driver_id')
        plate_number = self.request.query_params.get('plate_number')
        
        if vehicle_type:
            qs = qs.filter(vehicle_type=vehicle_type)
        if status_filter:
            qs = qs.filter(status=status_filter)
        if driver_id:
            qs = qs.filter(driver_id=driver_id)
        if plate_number:
            qs = qs.filter(plate_number__icontains=plate_number)
        return qs

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @cache_response(60 * 15)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        if many:
            instances = [Vehicle.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        if many:
            instances = [Vehicle.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, partial=True, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        ids = request.query_params.get('ids')
        if ids:
            ids_list = [int(pk) for pk in ids.split(',')]
            Vehicle.objects.filter(pk__in=ids_list).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)


class OrderViewSet(viewsets.ModelViewSet):
    """
    Представление для работы с заказами на перевозку.
    
    Фильтрация по статусу, адресу, весу и транспортному средству.
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        status_filter = self.request.query_params.get('status')
        pickup_address = self.request.query_params.get('pickup_address')
        delivery_address = self.request.query_params.get('delivery_address')
        vehicle_id = self.request.query_params.get('vehicle_id')
        min_weight = self.request.query_params.get('min_weight')
        
        if status_filter:
            qs = qs.filter(status=status_filter)
        if pickup_address:
            qs = qs.filter(pickup_address__icontains=pickup_address)
        if delivery_address:
            qs = qs.filter(delivery_address__icontains=delivery_address)
        if vehicle_id:
            qs = qs.filter(vehicle_id=vehicle_id)
        if min_weight:
            qs = qs.filter(weight_kg__gte=min_weight)
        return qs

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @cache_response(60 * 15)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """При создании заказа статус автоматически 'pending'."""
        serializer.save(status='pending')

    def update(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        if many:
            instances = [Order.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        if many:
            instances = [Order.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, partial=True, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        ids = request.query_params.get('ids')
        if ids:
            ids_list = [int(pk) for pk in ids.split(',')]
            Order.objects.filter(pk__in=ids_list).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)


class TrackingEventViewSet(viewsets.ModelViewSet):
    """
    Представление для событий отслеживания заказов.
    
    Создание событий доступно всем, изменение — только авторизованным.
    """
    serializer_class = TrackingEventSerializer
    queryset = TrackingEvent.objects.all()
    permission_classes = [IsDriverOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        order_id = self.request.query_params.get('order_id')
        if order_id:
            qs = qs.filter(order_id=order_id)
        return qs.order_by('-created_at')

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @cache_response(60 * 15)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """Автоматически подставляет текущего пользователя, если он авторизован."""
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)

    def update(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        if many:
            instances = [TrackingEvent.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        if many:
            instances = [TrackingEvent.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, partial=True, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        ids = request.query_params.get('ids')
        if ids:
            ids_list = [int(pk) for pk in ids.split(',')]
            TrackingEvent.objects.filter(pk__in=ids_list).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)