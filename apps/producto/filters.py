from django_filters.rest_framework import FilterSet, CharFilter
from .models import Producto


class ProductoFilter(FilterSet):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'stock']

    nombre = CharFilter(field_name='nombre', lookup_expr='icontains')