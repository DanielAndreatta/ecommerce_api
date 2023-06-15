import pytest
from apps.core.tests.fixtures import api_client, get_default_test_user
from apps.orden.models import DetalleOrden
from apps.orden.tests.fixtures import crear_ordenes2
from apps.producto.tests.fixtures import crear_productos


@pytest.mark.parametrize(
    'cantidad, codigo_http, total_registros, loguear_usuario',
    [(5, 403, 0, False),
     (5, 201, 1, True)]
)


@pytest.mark.django_db
def test_api_creacion_detalle_orden(api_client, get_default_test_user, crear_ordenes2, crear_productos,
                                    cantidad, codigo_http, total_registros, loguear_usuario):
    client = api_client
    if loguear_usuario:
        client.force_authenticate(user=get_default_test_user)

    orden1 = crear_ordenes2

    producto1, producto2, producto3 = crear_productos

    data = {
        "orden": orden1.id,
        "cantidad": cantidad,
        "precio_unitario": producto3.precio,
        "producto": producto3.id,
    }

    response = client.post(f'/api/v1/detalle_orden/', data=data)
    assert response.status_code == codigo_http

    assert DetalleOrden.objects.filter(
        orden=orden1, cantidad=cantidad, precio_unitario=producto3.precio, producto=producto3
    ).count() == total_registros