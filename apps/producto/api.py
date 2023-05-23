from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductoFilter

from rest_framework.viewsets import ModelViewSet
from .models import Producto
from .serializers import ProductoSerializer


class ProductoViewSet(ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    #filter_backends = [DjangoFilterBackend]
    #filterset_class = ProductoFilter
    ordering_fields = ['nombre']
    lookup_field = 'uuid'



