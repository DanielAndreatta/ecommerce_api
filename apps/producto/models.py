from uuid import uuid4
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Producto(models.Model):

    uuid = models.UUIDField(unique=True, editable=False, default=uuid4)
    nombre = models.CharField(max_length=50)
    precio = models.FloatField()
    stock = models.IntegerField(
        validators=[
            MinValueValidator(0, message='El stock debe ser mayor a 0.'),
            MaxValueValidator(100000, message='El stock debe ser menor a 100,000.')
        ]
    )

    class Meta:
        ordering = ('nombre',)

    def __str__(self):
        return '{}'.format(self.nombre)

    def sumar_stock(self, cantidad):
        self.stock += cantidad
        self.save()

    def restar_stock(self, cantidad):

        #if 0 < cantidad <= self.stock:
            self.stock -= cantidad
            self.save()
        #else:
            #raise ValueError("La cantidad ingresada es inválida o excede el stock disponible")



