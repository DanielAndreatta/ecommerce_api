
from rest_framework.serializers import ModelSerializer
from .models import Producto


class ProductoSerializer(ModelSerializer):
    class Meta:
        model = Producto
        fields = ['uuid', 'nombre', 'precio', 'stock']


class ProductoStockSerializer(ModelSerializer):
    class Meta:
        model = Producto
        fields = ['uuid', 'stock']