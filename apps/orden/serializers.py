
from rest_framework.serializers import ModelSerializer, ValidationError, SerializerMethodField, FloatField
from .models import Orden, DetalleOrden
import requests



class DetalleOrdenSerializer(ModelSerializer):

    precio_unitario = FloatField(read_only=True)

    class Meta:
        model = DetalleOrden
        fields = ['uuid', 'orden', 'cantidad', 'producto','precio_unitario']

    #Inciso 4) validar si hay suficiente stock. 
    #Inciso 5) validar que la cantidad del producto sea mayor a cero.
    def validate(self, atributos):
        producto = atributos['producto']
        cantidad = atributos['cantidad']

        if cantidad > producto.stock:
            raise ValidationError("No hay suficiente stock del producto.")

        if cantidad <= 0:
            raise ValidationError("La cantidad ingresada debe ser mayor a cero.")

        return atributos



class OrdenSerializer(ModelSerializer):
    total_orden_pesos = SerializerMethodField(method_name='get_total')
    total_orden_usd = SerializerMethodField(method_name='get_total_usd')
    detalle_orden = DetalleOrdenSerializer(many=True, read_only=True, source='detalles_orden')

    class Meta:
        model = Orden
        fields = ['uuid', 'fecha_hora','detalle_orden','total_orden_pesos','total_orden_usd']

    # Insciso 3)
    def get_total(self, orden):
        return orden.get_total_orden()

    def get_total_usd(self, orden):
        response = requests.get('https://www.dolarsi.com/api/api.php?type=valoresprincipales').json()
        dolar_blue = response[1]['casa']['venta'].replace(',', '.')
        cotizar_dolar = float(orden.get_total_orden()) / float(dolar_blue)
        return round(cotizar_dolar, 2)




