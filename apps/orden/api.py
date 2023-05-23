
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