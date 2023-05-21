
from rest_framework import viewsets
from .models import Orden,DetalleOrden
from .serializers import OrdenSerializer,DetalleOrdenSerializer


class OrdenViewSet(viewsets.ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer

class DetalleOrdenViewSet(viewsets.ModelViewSet):
    queryset = DetalleOrden.objects.all()
    serializer_class = DetalleOrdenSerializer