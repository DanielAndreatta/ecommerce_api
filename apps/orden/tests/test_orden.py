import pytest
import uuid
from apps.producto.models import Producto
from apps.orden.models import DetalleOrden, Orden
from apps.core.tests.fixtures import api_client, get_default_test_user
from apps.orden.tests.fixtures import crear_orden, crear_ordenes, crear_detalle_orden, crear_detalles_orden, crear_ordenes_con_detalles
from apps.producto.tests.fixtures import crear_producto, crear_productos
from datetime import datetime



#Inciso 1 (verificar que al ejecutar el endpoint de recuperación de una orden, este devuelva un status 400)

@pytest.mark.django_db
def test_api_recuperar_orden(api_client, get_default_test_user, crear_detalle_orden):

    client = api_client
    client.force_authenticate(user=get_default_test_user)

    detalle_orden = crear_detalle_orden

    response = client.get(f'/api/v1/orden/{detalle_orden.orden.uuid}/')

    assert response.status_code == 400

    assert Orden.objects.filter(
        uuid = detalle_orden.orden.uuid
    ).count() == 1



#Inciso 2 (crear detalle orden correctamente)

@pytest.mark.django_db
def test_api_creacion_detalle_orden(api_client, get_default_test_user, crear_producto, crear_orden):

    client = api_client
    client.force_authenticate(user=get_default_test_user)

    orden = crear_orden
    producto = crear_producto
    cantidad = 5

    # stock del producto igual a 50
    assert producto.stock == 50

    # Compruebo que la cantidad sea menor al stock del producto
    assert cantidad <= producto.stock

    data = {
        "orden": orden.id,
        "cantidad": cantidad,
        "precio_unitario": producto.precio,
        "producto": producto.id,
    }

    response = client.post(f'/api/v1/detalle_orden/', data=data)
    assert response.status_code == 201

    # Compruebo que se encuentre en la base de datos
    assert DetalleOrden.objects.filter(
        orden=orden, cantidad=5, precio_unitario=producto.precio, producto=producto
    ).count() == 1

    # Comprobar que se haya actualizado el stock del producto asociado al detalle (antes stock 50, ahora 45)
    producto.refresh_from_db()
    assert producto.stock == 45



#Inciso 3 (Verificar que al ejecutar el endpoint de creación de una orden, se produzca un fallo al intentar crear una orden cuyo detalle tenga productos repetidos.)

@pytest.mark.django_db
def test_api_fallo_crear_detalle_orden_con_producto_repetido(api_client, get_default_test_user, crear_detalles_orden, crear_productos):

    client = api_client
    client.force_authenticate(user=get_default_test_user)

    # Tenemos 1(una) orden con 2(dos) detalles(producto1 y producto3) en la base de datos
    detalle_orden1, detalle_orden2, orden = crear_detalles_orden
    producto1, producto2, producto3 = crear_productos

    data = {
        "orden": orden.id,
        "cantidad": 8,
        "precio_unitario": producto1.precio,
        "producto": producto1.id,
    }

    # Se quiere crear un detalle con el producto1, pero la orden ya posee el mismo producto, por lo que debe dar un status_code=400
    response = client.post(f'/api/v1/detalle_orden/', data=data)
    assert response.status_code == 400

    # Compruebo que solo se encuentren los 2(dos) detalles iniciales en la base de datos
    assert DetalleOrden.objects.filter(
        orden=orden
    ).count() == 2

    # Compruebo que solo hay un detalle con producto1 en la orden
    assert DetalleOrden.objects.filter(
        orden=orden, producto=producto1
    ).count() == 1



#Inciso 4 (Verificar que al ejecutar el endpoint de creación de una orden, se produzca un fallo al intentar crear una orden donde la cantidad de un producto del detalle, sea mayor al stock de ese producto.)

@pytest.mark.django_db
def test_api_fallo_crear_detalle_orden_con_cantidad_mayor_stock(api_client, get_default_test_user, crear_producto, crear_orden):

    client = api_client
    client.force_authenticate(user=get_default_test_user)

    orden = crear_orden
    producto = crear_producto

    # El stock de producto es igual a 50. Al ingresar cantidad 100, si hacemos un POST, no se debe crear el detalle
    data = {
        "orden": orden.id,
        "cantidad": 100,
        "precio_unitario": producto.precio,
        "producto": producto.id,
    }

    response = client.post(f'/api/v1/detalle_orden/', data=data)
    # se espera un status_code=400, ya que no se creo el detalle
    assert response.status_code == 400

    # Compruebo que no se ha creado el detalle
    assert DetalleOrden.objects.filter(orden=orden, producto=producto).exists() == False



#Inciso 5 (verificar que al ejecutar el endpoint de eliminación de una orden, ésta se haya eliminado de la base de datos correctamente, junto con su detalle, y que además, se haga incrementado el stock de producto relacionado con cada detalle de orden)

@pytest.mark.django_db
def test_api_eliminar_orden(api_client, get_default_test_user, crear_ordenes_con_detalles):

    client = api_client
    client.force_authenticate(user=get_default_test_user)

    # En la base de datos se encuentran dos ordenes: la orden1 con 2(dos) detalles, detalle_orden1(producto1) y detalle_orden2(producto3); tambien la orden2 con el detalle3(producto2)
    orden1, detalle_orden1, detalle_orden2, orden2, detalle_orden3, producto1, producto2, producto3 = crear_ordenes_con_detalles

    # Stock antes de eliminar la orden producto1=45, producto2=7, producto3=15
    assert producto1.stock == 40
    assert producto2.stock == 7
    assert producto3.stock == 15

    # Eliminamos la orden1, con sus dos detalles(detalle1, detalle2)
    response = client.delete(f'/api/v1/orden/{orden1.uuid}/')
    assert response.status_code == 204

    #Verificar el stock despues de eliminar la orden con sus detalles, en este caso se borraron el detalle1 con cantidad 10, y detalle2 con cantidad 5
    producto1.refresh_from_db()
    producto2.refresh_from_db()
    producto3.refresh_from_db()
    assert producto1.stock == 50  # Antes 40, +10 = 50
    assert producto2.stock == 7   # No sufre cambios
    assert producto3.stock == 20  # Antes 15, +5 = 20

    # Verificar que la orden y sus detalles se hayan eliminado de la base de datos
    assert Orden.objects.filter(uuid=orden1.uuid).exists() == False
    assert DetalleOrden.objects.filter(orden=orden1.id).exists() == False



#Inciso 7 (verificar que el método get_total de una orden, devuelve el valor correcto de acuerdo al total de cada detalle)
@pytest.mark.django_db
def test_api_get_total_orden(crear_detalles_orden):

    total_esperado = (300 * 10) + (800 * 5)
    detalle_orden1, detalle_orden2, orden= crear_detalles_orden
    total = orden.get_total_orden()
    assert total == total_esperado



#Inciso 8 (verificar que el método get_total_detalle de un detalle de orden, devuelve el valor correcto de acuerdo a al precio del producto y cantidad de la orden)
@pytest.mark.django_db
def test_api_get_total_detalle(crear_detalle_orden):

    total_esperado = 300 * 2
    total = crear_detalle_orden.get_total_detalle()
    assert total == total_esperado


# Test unitario para verificar que se crea una orden correctamente
@pytest.mark.django_db
def test_crear_orden():
    fecha_hora = datetime.strptime('2024-04-27T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ')

    orden = Orden(fecha_hora=fecha_hora)

    assert orden is not None
    assert orden.fecha_hora == fecha_hora


# Test unitario para verificar que se crea un detalle_orden correctamente
@pytest.mark.django_db
def test_crear_detalle_orden():

    producto = Producto(nombre="Cuaderno", precio=4000, stock=100)

    fecha_hora = datetime.strptime('2024-04-27T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    orden = Orden(fecha_hora=fecha_hora)

    detalle_orden = DetalleOrden(orden=orden, cantidad=5, precio_unitario=producto.precio, producto=producto)

    assert detalle_orden is not None
    assert detalle_orden.orden == orden
    assert detalle_orden.cantidad == 5
    assert detalle_orden.precio_unitario == producto.precio
    assert detalle_orden.producto == producto


