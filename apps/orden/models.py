
from django.db import models
from datetime import datetime
from apps.producto.models import Producto

class Orden(models.Model):

    fecha_hora = models.DateTimeField(default=datetime.today)

class DetalleOrden(models.Model):

    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='ordenes')
    cantidad = models.IntegerField()
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='productos')
