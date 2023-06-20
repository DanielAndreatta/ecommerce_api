import pytest
import uuid
from apps.orden.models import DetalleOrden, Orden
from apps.core.tests.fixtures import api_client, get_default_test_user
from apps.orden.tests.fixtures import crear_ordenes, crear_detalle_orden, crear_orden, crear_detalles_orden
from apps.producto.tests.fixtures import crear_productos
from datetime import datetime
from rest_framework.test import APIClient


@pytest.mark.parametrize(
    'codigo_http, total_registros',
    [(200, 2)]
)

#Se devuelven todas las ordenes (GET)
@pytest.mark.django_db
def test_api_listar_ordenes(api_client, get_default_test_user, crear_ordenes, codigo_http, total_registros):

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
    [(200, 1)]
)

#Inciso 1 (verificar que al ejecutar el endpoint de recuperación de una orden, se devuelven los datos correctos de la orden y su detalle)
@pytest.mark.django_db
def test_api_recuperar_orden(api_client, get_default_test_user, crear_detalle_orden, codigo_http, total_registros):

    client = api_client
    client.force_authenticate(user=get_default_test_user)

    detalle_orden = crear_detalle_orden

    response = client.get(f'/api/v1/orden/{detalle_orden.orden.uuid}/')

    assert response.status_code == codigo_http

    assert DetalleOrden.objects.filter(
        id = detalle_orden.orden.id
    ).count() == total_registros

    #Guarda los datos obtenidos de la respuesta de la solicitud HTTP en formato JSON.
    json_data = response.json()

    #print(json_data)
    #print(detalle_orden.orden.uuid)
    #print(detalle_orden.uuid)
    #print(detalle_orden.producto.id)

    assert uuid.UUID(json_data['uuid']) == detalle_orden.orden.uuid
    assert json_data['fecha_hora'] == '2023-06-12T00:00:00Z'
    assert json_data['total_orden_pesos'] == 3000
    assert json_data['total_orden_usd'] == 6.1

    primer_detalle = json_data['detalle_orden'][0]

    assert uuid.UUID(primer_detalle['uuid']) == detalle_orden.uuid
    assert primer_detalle['cantidad'] == 2
    assert primer_detalle['producto'] == detalle_orden.producto.id
    assert primer_detalle['precio_unitario'] == 1500


@pytest.mark.parametrize(
    'cantidad, codigo_http, total_registros, loguear_usuario',
    [(5, 403, 0, False),
     (5, 201, 1, True)]
)

#Inciso 2 (crear orden correctamente)
@pytest.mark.django_db
def test_api_creacion_orden(api_client, get_default_test_user, crear_orden, crear_productos,
                                    cantidad, codigo_http, total_registros, loguear_usuario):
    client = api_client
    if loguear_usuario:
        client.force_authenticate(user=get_default_test_user)

    """
    data1 = {
        "orden": orden.id,
        "cantidad": cantidad,
        "precio_unitario": producto3.precio,
        "producto": producto3.id,
    }

    data = {
        'fecha_hora': '2020-05-11',
        'detalles_orden': [
            {'producto': producto.id, 'cantidad': 2},
        ]
    }

    response = client.post(f'/api/v1/detalle_orden/', data=data)
    assert response.status_code == codigo_http

    assert DetalleOrden.objects.filter(
        orden=orden, cantidad=cantidad, precio_unitario=producto3.precio, producto=producto3
    ).count() == total_registros
    """


#Inciso 7 (verificar que el método get_total de una orden, devuelve el valor correcto de acuerdo al total de cada detalle)
@pytest.mark.django_db
def test_api_get_total_orden(crear_detalles_orden):

    total_esperado = (300 * 10) + (800 * 5)
    detalle_orden1, detalle_orden2 = crear_detalles_orden
    total = detalle_orden1.orden.get_total_orden()
    assert total == total_esperado


#Inciso 8 (verificar que el método get_total_detalle de un detalle de orden, devuelve el valor correcto de acuerdo a al precio del producto y cantidad de la orden)
@pytest.mark.django_db
def test_api_get_total_detalle(crear_detalle_orden):

    total_esperado = 1500 * 2
    total = crear_detalle_orden.get_total_detalle()
    assert total == total_esperado


