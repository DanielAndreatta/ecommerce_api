
from rest_framework.viewsets import ModelViewSet
from .models import Orden, DetalleOrden, Producto
from .serializers import OrdenSerializer, DetalleOrdenSerializer
from rest_framework.response import Response
from rest_framework import status
from .filters import OrdenFilter, DetalleOrdenFilter



class OrdenViewSet(ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer
    filterset_class = OrdenFilter
    ordering_fields = ['fecha_hora']
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

        # Restar el stock del producto al crear un detalle de orden
        producto = serializer.validated_data['producto']
        cantidad = serializer.validated_data['cantidad']
        precio_uni = producto.precio
        producto.restar_stock(cantidad)
        serializer.save(precio_unitario=precio_uni)


    def perform_update(self, serializer):
        # Obtener el producto anterior y el nuevo producto
        producto_anterior = serializer.instance.producto
        producto_nuevo = serializer.validated_data['producto']
        # Obtener la cantidad anterior y nueva
        cantidad_anterior = serializer.instance.cantidad
        cantidad_nueva = serializer.validated_data['cantidad']

        #print("PRODUCTO ANTERIOR:", producto_anterior)
        #print("PRODUCTO NUEVO:", producto_nuevo)
        #print("stock_anterior:", producto_anterior.stock)
        #print("stock_nuevo:", producto_nuevo.stock)
        #print("Valor de cantidad_anterior:", cantidad_anterior)
        #print("Valor de cantidad_nueva:", cantidad_nueva)

        # Reestablecer el stock del producto anterior solo si el producto ha cambiado
        if producto_anterior != producto_nuevo:
            producto_anterior.sumar_stock(cantidad_anterior)
        # Restar el stock del producto anterior solo si el producto ha cambiado
        if producto_anterior != producto_nuevo:
            producto_nuevo.restar_stock(cantidad_nueva)

        if producto_anterior == producto_nuevo:
            # Calcular la diferencia de cantidad
            stock_total = producto_nuevo.stock + cantidad_anterior
            cantidad_diferencia = stock_total - cantidad_nueva
            # Restar la diferencia al stock del producto nuevo
            producto_nuevo.reestablecer_stock(cantidad_diferencia)
       
        # Actualizar el precio_unitario con el nuevo precio del producto
        serializer.instance.precio_unitario = producto_nuevo.precio
        # Actualizar la cantidad en el detalle de orden
        serializer.instance.cantidad = cantidad_nueva
        # Guardar los cambios en el detalle de orden
        serializer.save()


    def perform_destroy(self, instance):
        # Sumar el stock del producto al eliminar un detalle de orden
        producto = instance.producto
        producto.sumar_stock(instance.cantidad)
        instance.delete()