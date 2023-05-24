from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response

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









    """def perform_create(self, serializer):
        # controlar que no se registren mas de 1 unidad de tipo-asistencia del tipo="comida"
        tipo_asistencia = serializer.validated_data.get('tipo_asistencia', None)
        cantidad = serializer.validated_data.get('cantidad', None)

        if tipo_asistencia.tipo == TipoAsistencia.COMIDA and cantidad > 1:
            raise ValidationError('La cantidad no puede ser mayor a 1 para asistencia de comida.')

        super().perform_create(serializer)


class ProductoListCreateViewListCreateView(ListCreateAPIView):
    queryset = AsignacionBeneficio.objects.all()
    serializer_class = AsignacionBeneficioSerializer

    # se sobrescribe el metodo para listar solo los beneficios del programa indicado en la URL
    def list(self, request, *args, **kwargs):
        programa = get_object_or_404(Programa, pk=kwargs['pk'])

        queryset = self.filter_queryset(self.get_queryset())

        # se filtran registros
        queryset = queryset.filter(programa=programa)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)"""



