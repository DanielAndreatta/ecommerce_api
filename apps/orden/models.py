from uuid import uuid4
from django.db import models
from datetime import datetime
from apps.producto.models import Producto
from decimal import Decimal


class Orden(models.Model):

    uuid = models.UUIDField(unique=True, editable=False, default=uuid4)
    fecha_hora = models.DateTimeField(default=datetime.today)


    # Insciso 3)
    def get_total_orden(self):
        total_orden = 0
        for detalle in self.detalles_orden.all():
            total_orden = total_orden + detalle.get_total_detalle()
        return total_orden

    class Meta:
        ordering = ('fecha_hora',)
    
    def __str__(self):
        fecha_hora_formateada = self.fecha_hora.strftime("%d/%m/%Y %H:%M:%S")
        return 'Fecha_hora: {}'.format(fecha_hora_formateada)




class DetalleOrden(models.Model):

    uuid = models.UUIDField(unique=True, editable=False, default=uuid4)
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='detalles_orden')
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='detalles_producto')

    class Meta:
        ordering = ('orden',)

    #inciso 3)
    def get_total_detalle(self):
        total_detalle = Decimal(self.precio_unitario) * int(self.cantidad)
        return round(total_detalle, 2)





