import pytest
from apps.core.tests.fixtures import api_client, get_default_test_user
from apps.orden.tests.fixtures import crear_ordenes, crear_detalle_orden, crear_orden
from apps.producto.tests.fixtures import crear_productos


@pytest.mark.parametrize(
    'codigo_http, total_registros',
    [(200, 2)]
)


#Inciso 1 (verificar que al ejecutar el endpoint de recuperación de una orden, se devuelven los datos correctos de la orden y su detalle)
@pytest.mark.django_db
def test_api_lista_ordenes(api_client, get_default_test_user, crear_ordenes, codigo_http, total_registros):

    client = api_client

    client.force_authenticate(user=get_default_test_user)

    response = client.get(f'/api/v1/orden/')

    assert response.status_code == codigo_http

    json_data = response.json()

    assert len(json_data) == total_registros

    assert json_data[0]['fecha_hora'] == '2023-06-12T00:00:00Z'

    assert json_data[1]['fecha_hora'] == '2020-05-11T00:00:00Z'


#Inciso 7 (verificar que el método get_total de una orden, devuelve el valor correcto de acuerdo al total de cada detalle)
@pytest.mark.django_db
def test_get_total_orden(crear_detalle_orden):

    total_esperado = 1500 * 2
    total = crear_detalle_orden.get_total_detalle()
    assert total == total_esperado


