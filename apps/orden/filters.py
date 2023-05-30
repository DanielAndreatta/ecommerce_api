from django_filters.rest_framework import FilterSet, CharFilter, DateFilter, NumberFilter
from .models import Orden, DetalleOrden
from django.forms import widgets

class OrdenFilter(FilterSet):
    
    class Meta:
        model = Orden
        fields = ['uuid', 'fecha', 'detalle_orden']

    detalle_orden = CharFilter(field_name='detalles_orden__id')
    fecha = DateFilter(field_name='fecha_hora', lookup_expr='date', widget=widgets.DateInput(attrs={'placeholder': 'Ejemplo: YYYY-MM-DD'}))



class DetalleOrdenFilter(FilterSet):
    
    class Meta:
        model = DetalleOrden
        fields = ['uuid', 'orden', 'max_cantidad', 'min_cantidad', 'producto','max_precio_unitario', 'min_precio_unitario']

    max_cantidad = NumberFilter(field_name='precio_unitario', lookup_expr='lte')
    min_cantidad = NumberFilter(field_name='precio_unitario', lookup_expr='gte')
    max_precio_unitario = NumberFilter(field_name='precio_unitario', lookup_expr='lte')
    min_precio_unitario = NumberFilter(field_name='precio_unitario', lookup_expr='gte')