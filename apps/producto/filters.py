from django_filters.rest_framework import FilterSet, CharFilter, NumberFilter
from .models import Producto


class ProductoFilter(FilterSet):
    
    class Meta:
        model = Producto
        fields = ['uuid','nombre','precio', 'min_precio', 'stock']

    min_precio = NumberFilter(field_name='precio', lookup_expr='gte')
    nombre = CharFilter(field_name='nombre', lookup_expr='icontains')

    