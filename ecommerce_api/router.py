from django.urls import path
from rest_framework import routers
from apps.producto import api as api_producto
from apps.orden import api as api_orden

router = routers.DefaultRouter()

# Registrar los ViewSet
router.register('producto', api_producto.ProductoViewSet)
router.register('orden', api_orden.OrdenViewSet)
router.register('detalle_orden', api_orden.DetalleOrdenViewSet)



"""urlpatterns = [
    path('persona/<uuid:uuid>/estado-salud/', EstadoSaludListCreateView.as_view()),
    path('programa/<int:pk>/asignacion-beneficio/', AsignacionBeneficioListCreateView.as_view()),
]"""

urlpatterns = router.urls