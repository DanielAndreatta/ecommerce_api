
from rest_framework.serializers import ModelSerializer, ValidationError, SerializerMethodField, FloatField
from .models import Orden, DetalleOrden
import requests



class DetalleOrdenSerializer(ModelSerializer):

    precio_unitario = FloatField(write_only=True)

    class Meta:
        model = DetalleOrden
        fields = ['id','orden', 'cantidad', 'producto','precio_unitario']



    #Inciso 4) validar que exista una cantidad del stock del producto
    def validate(self, atributos):
        # Obtiene el producto y la cantidad del detalle de orden
        producto = atributos['producto']
        cantidad = atributos['cantidad']

        # Valida que la cantidad no sea negativa
        if cantidad < 0:
            raise ValidationError("la cantidad ingresada debe ser mayor a cero.")


        # Valida si hay suficiente stock
        if cantidad > producto.stock:
            raise ValidationError("No hay suficiente stock del producto.")

        return atributos



class OrdenSerializer(ModelSerializer):
    total_orden = SerializerMethodField(method_name='get_total')
    total_orden_usd = SerializerMethodField(method_name='get_total_usd')
    #detalles_orden = SerializerMethodField(method_name='get_detalle_orden')
    detalles_orden = DetalleOrdenSerializer(many=True).allow_null       #read_only=True

    class Meta:
        model = Orden
        fields = ['id', 'fecha_hora', 'total_orden', 'total_orden_usd']
        #fields = ['id','fecha_hora','detalles_orden','total_orden','total_orden_usd']


    #def get_detalle_orden(self):
    #    return self.detalle_orden


    # Insciso 3)
    def get_total(self, orden):
        return orden.get_total_orden()

    def get_total_usd(self, orden):
        response = requests.get('https://www.dolarsi.com/api/api.php?type=valoresprincipales').json()
        dolar_blue = response[1]['casa']['venta'].replace(',', '.')
        cotizar_dolar = float(orden.get_total_orden()) / float(dolar_blue)
        return round(cotizar_dolar, 2)




