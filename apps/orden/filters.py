from django_filters.rest_framework import FilterSet, CharFilter, DateFilter, NumberFilter
from .models import Orden, DetalleOrden


class OrdenFilter(FilterSet):
    
    class Meta:
        model = Orden
        fields = ['id','fecha', 'detalle_orden']

    detalle_orden = CharFilter(field_name='detalles_orden__id')
    fecha = DateFilter(field_name='fecha_hora', lookup_expr='date')



class DetalleOrdenFilter(FilterSet):
    
    class Meta:
        model = DetalleOrden
        fields = ['id','orden', 'cantidad', 'producto','precio_unitario', 'max_precio_unitario', 'min_precio_unitario']

    max_precio_unitario = NumberFilter(field_name='precio_unitario', lookup_expr='lte')
    min_precio_unitario = NumberFilter(field_name='precio_unitario', lookup_expr='gte')