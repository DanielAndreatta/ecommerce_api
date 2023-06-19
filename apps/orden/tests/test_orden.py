import pytest
from apps.core.tests.fixtures import api_client, get_default_test_user
from apps.orden.tests.fixtures import crear_ordenes, crear_detalle_orden, crear_orden, crear_detalles_orden
from apps.producto.tests.fixtures import crear_productos
from datetime import datetime


@pytest.mark.parametrize(
    'codigo_http, total_registros',
    [(200, 2)]
)

#Se devuelven todas las ordenes (GET)
@pytest.mark.django_db
def test_api_listar_orden(api_client, get_default_test_user, crear_ordenes, codigo_http, total_registros):

    client = api_client
    client.force_authenticate(user=get_default_test_user)

    response = client.get(f'/api/v1/orden/')

    assert response.status_code == codigo_http

    json_data = response.json()

    assert len(json_data) == total_registros

    assert json_data[0]['fecha_hora'] == '2023-06-12T00:00:00Z'

    assert json_data[1]['fecha_hora'] == '2020-05-11T00:00:00Z'



@pytest.mark.parametrize(
    'codigo_http, total_registros',
    [(404, 1)]
)

#Inciso 1 (verificar que al ejecutar el endpoint de recuperación de una orden, se devuelven los datos correctos de la orden y su detalle)
@pytest.mark.django_db
def test_api_recuperar_ordenes(api_client, get_default_test_user, crear_orden, crear_productos, crear_detalles_orden, codigo_http, total_registros):

    client = api_client
    client.force_authenticate(user=get_default_test_user)

    orden = crear_orden

    #response = client.get(f'/api/v1/orden/{detalle_orden1.orden.id}/')
    response = client.get(f'/api/v1/orden/1/')

    assert response.status_code == codigo_http

    json_data = response.json()
    
    assert len(json_data) == total_registros

    assert json_data[0]['fecha_hora'] == '2023-06-12T00:00:00Z'
    #fecha_hora_orden = datetime.strptime(json_data[0]['fecha_hora'], "%Y-%m-%dT%H:%M:%SZ")
    #assert fecha_hora_orden == datetime(2023, 6, 12, 0, 0, 0)



@pytest.mark.parametrize(
    'cantidad, codigo_http, total_registros, loguear_usuario',
    [(5, 403, 0, False),
     (5, 201, 1, True)]
)

#Inciso 2
@pytest.mark.django_db
def test_api_creacion_detalle_orden(api_client, get_default_test_user, crear_orden, crear_productos,
                                    cantidad, codigo_http, total_registros, loguear_usuario):
    client = api_client
    if loguear_usuario:
        client.force_authenticate(user=get_default_test_user)

    orden = crear_orden

    producto1, producto2, producto3 = crear_productos

    data = {
        "orden": orden.id,
        "cantidad": cantidad,
        "precio_unitario": producto3.precio,
        "producto": producto3.id,
    }

    response = client.post(f'/api/v1/detalle_orden/', data=data)
    assert response.status_code == codigo_http

    assert DetalleOrden.objects.filter(
        orden=orden, cantidad=cantidad, precio_unitario=producto3.precio, producto=producto3
    ).count() == total_registros






#Inciso 7 (verificar que el método get_total de una orden, devuelve el valor correcto de acuerdo al total de cada detalle)
@pytest.mark.django_db
def test_api_get_total_orden(crear_detalle_orden):

    total_esperado = 1500 * 2
    total = crear_detalle_orden.get_total_detalle()
    assert total == total_esperado


