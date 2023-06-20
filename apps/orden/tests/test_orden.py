import pytest
import uuid
from apps.orden.models import DetalleOrden, Orden
from apps.core.tests.fixtures import api_client, get_default_test_user
from apps.orden.tests.fixtures import crear_ordenes, crear_detalle_orden, crear_orden, crear_detalles_orden
from apps.producto.tests.fixtures import crear_productos
from datetime import datetime
from rest_framework.test import APIClient



#Se devuelven todas las ordenes (GET)
@pytest.mark.parametrize(
    'codigo_http, total_registros, loguear_usuario',
    [(200, 2, True)]
)
@pytest.mark.django_db
def test_api_listar_ordenes(api_client, get_default_test_user, crear_ordenes,
                                                    codigo_http, total_registros, loguear_usuario):

    client = api_client
    if loguear_usuario:
        client.force_authenticate(user=get_default_test_user)

    response = client.get(f'/api/v1/orden/')

    assert response.status_code == codigo_http

    json_data = response.json()

    assert len(json_data) == total_registros

    assert json_data[0]['fecha_hora'] == '2023-06-12T00:00:00Z'

    assert json_data[1]['fecha_hora'] == '2020-05-11T00:00:00Z'



#Inciso 1 (verificar que al ejecutar el endpoint de recuperación de una orden, se devuelven los datos correctos de la orden y su detalle)
@pytest.mark.parametrize(
    'codigo_http, total_registros, loguear_usuario',
    [(200, 1, True)]
)
@pytest.mark.django_db
def test_api_recuperar_orden(api_client, get_default_test_user, crear_detalle_orden,
                                                        codigo_http, total_registros, loguear_usuario):

    client = api_client
    if loguear_usuario:
        client.force_authenticate(user=get_default_test_user)

    detalle_orden = crear_detalle_orden

    response = client.get(f'/api/v1/orden/{detalle_orden.orden.uuid}/')

    assert response.status_code == codigo_http

    assert Orden.objects.filter(
        uuid = detalle_orden.orden.uuid
    ).count() == total_registros

    #Guarda los datos obtenidos de la respuesta de la solicitud HTTP en formato JSON.
    json_data = response.json()

    print(json_data)
    assert uuid.UUID(json_data['uuid']) == detalle_orden.orden.uuid
    assert json_data['fecha_hora'] == '2023-06-12T00:00:00Z'
    assert json_data['total_orden_pesos'] == 3000

    primer_detalle = json_data['detalle_orden'][0]
    assert uuid.UUID(primer_detalle['uuid']) == detalle_orden.uuid
    assert primer_detalle['cantidad'] == 2
    assert primer_detalle['producto'] == detalle_orden.producto.id
    assert primer_detalle['precio_unitario'] == 1500



#Inciso 2 (crear orden correctamente)
@pytest.mark.parametrize(
    'codigo_http, codigo_http_producto_repetido, codigo_http_cantidad, total_registros, loguear_usuario',
    [(201, 400, 400, 1, True), #Inciso 2 APROBADO al crear una orden, con dos detalles orden
     (201, 201, 400, 1, True), #Inciso 3 FALLO al crear Producto repetido en la orden
     (201, 400, 201, 1, True)] #Inciso 4 FALLO al haber Cantidad menor o igual al stock del producto
)
@pytest.mark.django_db
def test_api_creacion_orden(api_client, get_default_test_user, crear_orden, crear_productos,
                            codigo_http, codigo_http_producto_repetido, codigo_http_cantidad, total_registros, loguear_usuario):
    
    client = api_client
    if loguear_usuario:
        client.force_authenticate(user=get_default_test_user)

    producto1, producto2, producto3 = crear_productos

    orden = crear_orden

    #print(detalle_orden1)

    data_orden = {
        'fecha_hora': orden.fecha_hora
    }

    data_detalle1 = {
        "orden": orden.id,
        "cantidad": 5,
        "precio_unitario": producto1.precio,
        "producto": producto1.id,
    }

    data_detalle2 = {
        "orden": orden.id,
        "cantidad": 3,
        "precio_unitario": producto3.precio,
        "producto": producto3.id,
    }

    data_detalle3 = {
        "orden": orden.id,
        "cantidad": 150,
        "precio_unitario": producto3.precio,
        "producto": producto2.id,
    }

    response_orden = client.post(f'/api/v1/orden/', data=data_orden)
    response_detalle1 = client.post(f'/api/v1/detalle_orden/', data=data_detalle1)
    response_detalle2 = client.post(f'/api/v1/detalle_orden/', data=data_detalle2)
    #Cantidad menor o igual al stock del producto
    response_detalle3 = client.post(f'/api/v1/detalle_orden/', data=data_detalle3)
    #Producto repetido en la orden
    response_detalle4 = client.post(f'/api/v1/detalle_orden/', data=data_detalle2)

    assert response_orden.status_code == codigo_http
    assert response_detalle1.status_code == codigo_http
    assert response_detalle2.status_code == codigo_http
    #Se espera un status_code = 400 , porque la cantidad es menor o igual al stock del producto
    assert response_detalle3.status_code == codigo_http_cantidad
    #Se espera un status_code = 400 , porque el producto ya se encuentra en la orden
    assert response_detalle4.status_code == codigo_http_producto_repetido

    # Verificar que se haya creado correctamente
    assert Orden.objects.filter(
        uuid=orden.uuid
    ).count() == total_registros

    response = client.get(f'/api/v1/orden/{orden.uuid}/')
    json_data = response.json()

    print(json_data)
    assert uuid.UUID(json_data['uuid']) == orden.uuid
    assert json_data['fecha_hora'] == '2023-06-12T00:00:00Z'
    assert json_data['total_orden_pesos'] == 3900


    # Realiza una consulta a la base de datos para obtener los valores más recientes de los campos del objeto y los actualiza en el objeto en memoria.
    producto1.refresh_from_db()
    producto3.refresh_from_db()
    #actualizado el stock del producto
    assert producto1.stock == 45
    assert producto3.stock == 17



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


