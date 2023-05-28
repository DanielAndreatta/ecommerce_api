from django_filters.rest_framework import FilterSet, CharFilter, NumberFilter
from .models import Producto


class ProductoFilter(FilterSet):
    
    class Meta:
        model = Producto
        fields = ['uuid','nombre', 'min_precio', 'max_precio', 'min_stock', 'max_stock' ]

    max_precio = NumberFilter(field_name='precio', lookup_expr='lte')
    min_precio = NumberFilter(field_name='precio', lookup_expr='gte')
    max_stock = NumberFilter(field_name='stock', lookup_expr='lte')
    min_stock = NumberFilter(field_name='stock', lookup_expr='gte')

    nombre = CharFilter(field_name='nombre', lookup_expr='icontains')

    