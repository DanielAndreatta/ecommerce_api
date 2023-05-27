
from django.db import models
from datetime import datetime
from apps.producto.models import Producto


class Orden(models.Model):

    fecha_hora = models.DateTimeField(default=datetime.today)


    # Insciso 3)
    def get_total_orden(self):
        total_orden = 0
        for detalle in self.detalles_orden.all():
            total_orden = total_orden + detalle.get_total_detalle()
        return total_orden

    #def get_uuid(self):
    #    uuid = self.id
    #    return uuid

    
    def __str__(self):
        fecha_hora_formateada = self.fecha_hora.strftime("%d/%m/%Y %H:%M:%S")
        return 'Fecha_hora: {}'.format(fecha_hora_formateada)




class DetalleOrden(models.Model):

    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='detalles_orden')
    cantidad = models.IntegerField()
    precio_unitario = models.FloatField()
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='detalles_producto')

    #inciso 3)
    def get_total_detalle(self):
        total_detalle = self.precio_unitario * self.cantidad
        return total_detalle

    # inciso 5)

    def clean(self):
        # Validar que la cantidad sea mayor a 0
        if self.cantidad <= 0:
            raise models.ValidationError('La cantidad del producto debe ser mayor a 0.')

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        # Validar que no se repita el producto en el mismo pedido
        detalles_orden = self.orden.detalles_orden.all()
        productos = [detalle.producto for detalle in detalles_orden if detalle != self]
        if self.producto in productos:
            raise models.ValidationError('No se permiten productos duplicados en el mismo pedido.')

