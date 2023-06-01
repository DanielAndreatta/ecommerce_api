from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from .models import Orden, DetalleOrden, Producto
from .serializers import OrdenSerializer, DetalleOrdenSerializer
#from rest_framework.response import Response
from rest_framework import status
from .filters import OrdenFilter, DetalleOrdenFilter



class OrdenViewSet(ModelViewSet):
    queryset = Orden.objects.all().order_by('-fecha_hora')
    serializer_class = OrdenSerializer
    filterset_class = OrdenFilter
    lookup_field = 'uuid'


    def perform_destroy(self, instance):
        # Restablecer el stock de los productos asociados a la orden
        detalles = instance.detalles_orden.all()
        for detalle in detalles:
            producto = detalle.producto
            producto.stock += detalle.cantidad
            producto.save()
        # Eliminar la orden
        instance.delete()




class DetalleOrdenViewSet(ModelViewSet):
    queryset = DetalleOrden.objects.all()
    serializer_class = DetalleOrdenSerializer
    filterset_class = DetalleOrdenFilter
    ordering_fields = ['orden']
    lookup_field = 'uuid'

    def perform_create(self, serializer):
        producto = serializer.validated_data['producto']
        cantidad = serializer.validated_data['cantidad']
        orden = serializer.validated_data['orden']

        # Inciso 5) Validar si ya existe un detalle con el mismo producto en esta orden
        if orden.detalles_orden.filter(producto=producto).exists():
            raise ValidationError('Ya existe un detalle con el mismo producto en esta orden.')

        precio_uni = producto.precio
        # Restar el stock del producto al crear un detalle de orden
        producto.restar_stock(cantidad)
        serializer.save(precio_unitario=precio_uni)


    def perform_update(self, serializer):
        producto_anterior = serializer.instance.producto
        producto_nuevo = serializer.validated_data['producto']
        cantidad_anterior = serializer.instance.cantidad
        cantidad_nueva = serializer.validated_data['cantidad']

        if producto_anterior != producto_nuevo:
            orden = serializer.instance.orden
            # Inciso 5) Validar si ya existe un detalle con el producto nuevo en esta orden
            if orden.detalles_orden.exclude(uuid=serializer.instance.uuid).filter(producto=producto_nuevo).exists():
                raise ValidationError('Ya existe un detalle con el mismo producto en esta orden.')
            producto_anterior.sumar_stock(cantidad_anterior)
            producto_nuevo.restar_stock(cantidad_nueva)

        if producto_anterior == producto_nuevo:
            stock_total = producto_nuevo.stock + cantidad_anterior
            cantidad_diferencia = stock_total - cantidad_nueva
            producto_nuevo.reestablecer_stock(cantidad_diferencia)
    
        serializer.instance.precio_unitario = producto_nuevo.precio
        serializer.instance.cantidad = cantidad_nueva
        serializer.save()


    def perform_destroy(self, instance):
        # Sumar el stock del producto al eliminar un detalle de orden
        producto = instance.producto
        producto.sumar_stock(instance.cantidad)
        instance.delete()