"""from django.urls import path
from rest_framework import routers
#from apps.persona import api as api_persona
#from apps.persona.api import EstadoSaludListCreateView
#from apps.programa import api as api_programa


# Initializar el router de DRF solo una vez
#from apps.programa.api import AsignacionBeneficioListCreateView

router = routers.DefaultRouter()

# Registrar los ViewSet
#router.register('persona', api_persona.PersonaViewSet)
#router.register('estado-salud', api_persona.EstadoSaludViewSet)
#router.register('programa', api_programa.ProgramaViewSet)
#router.register('asignacion-beneficio', api_programa.AsignacionBeneficioViewSet)


urlpatterns = [
    #path('persona/<uuid:uuid>/estado-salud/', EstadoSaludListCreateView.as_view()),
    #path('programa/<int:pk>/asignacion-beneficio/', AsignacionBeneficioListCreateView.as_view()),
]

urlpatterns += router.urls"""