
from rest_framework.viewsets import ModelViewSet
from .models import Orden, DetalleOrden
from .serializers import OrdenSerializer, DetalleOrdenSerializer
from rest_framework.response import Response
from rest_framework import status


class OrdenViewSet(ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer

    #def perform_destroy(self, instance):
        # Restablecer el stock de los productos asociados a la orden
    #    detalles = instance.detalles_orden.all()
    #    for detalle in detalles:
    #        producto = detalle.producto
    #        producto.stock += detalle.cantidad
    #        producto.save()

        # Eliminar la orden
    #    instance.delete()


class DetalleOrdenViewSet(ModelViewSet):
    queryset = DetalleOrden.objects.all()
    serializer_class = DetalleOrdenSerializer

    def perform_create(self, serializer):
        # Restar el stock del producto al crear un detalle de orden
        producto = serializer.validated_data['producto']
        cantidad = serializer.validated_data['cantidad']
        producto.restar_stock(cantidad)
        serializer.save()

    def perform_update(self, serializer):
        # Actualizar el stock del producto al modificar un detalle de orden
        producto = serializer.validated_data['producto']
        cantidad = serializer.validated_data['cantidad']
        producto.restar_stock(cantidad - serializer.instance.cantidad)
        serializer.save()

    def perform_destroy(self, instance):
        # Sumar el stock del producto al eliminar un detalle de orden
        producto = instance.producto
        producto.sumar_stock(instance.cantidad)
        instance.delete()