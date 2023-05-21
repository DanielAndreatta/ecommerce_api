
from django.db import models


class Producto(models.Model):

    nombre = models.CharField(max_length=50)
    precio = models.FloatField()
    stock = models.IntegerField()




