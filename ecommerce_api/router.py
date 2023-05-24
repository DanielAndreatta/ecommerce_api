from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.producto.api import ProductoViewSet
from apps.orden.api import OrdenViewSet,DetalleOrdenViewSet

router = DefaultRouter()

# Registrar los ViewSet
router.register('producto', ProductoViewSet)
router.register('orden', OrdenViewSet)
router.register('detalle_orden', DetalleOrdenViewSet)



"""urlpatterns = [
    path('producto/<uuid:uuid>', ProductoListCreateView.as_view()),
    #path('programa/<int:pk>/asignacion-beneficio/', AsignacionBeneficioListCreateView.as_view()),
]"""

urlpatterns = router.urls