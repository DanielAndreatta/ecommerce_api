from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from .filters import ProductoFilter

from rest_framework.viewsets import ModelViewSet
from .models import Producto
from .serializers import ProductoSerializer, ProductoStockSerializer


class ProductoViewSet(ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filterset_class = ProductoFilter
    ordering_fields = ['nombre']
    lookup_field = 'uuid'



class ProductoStockUpdateView(UpdateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoStockSerializer
    lookup_field = 'uuid'





