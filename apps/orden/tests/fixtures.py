import pytest
from apps.orden.models import DetalleOrden, Orden
from datetime import datetime


def crear_orden_con_parametros(fecha_hora):
    orden, _ = Orden.objects.get_or_create(
        fecha_hora=fecha_hora
    )
    return orden


def crear_detalle_orden_con_parametros(orden, cantidad, precio_unitario, producto):
    detalle_orden, _ = DetalleOrden.objects.get_or_create(
        orden=orden,
        cantidad=cantidad,
        precio_unitario=precio_unitario,
        producto=producto
    )

    return detalle_orden



@pytest.fixture
def crear_orden():

    fecha_hora = datetime.strptime('2023-06-12', '%Y-%m-%d')
    orden = crear_orden_con_parametros(fecha_hora)

    return orden


@pytest.fixture
def crear_ordenes():

    fecha_hora1 = datetime.strptime('2023-06-12', '%Y-%m-%d')
    orden1 = crear_orden_con_parametros(fecha_hora1)
    fecha_hora2 = datetime.strptime('2023-10-23', '%Y-%m-%d')
    orden2 = crear_orden_con_parametros(fecha_hora2)

    return orden1, orden2


@pytest.fixture
def crear_detalle_orden(crear_producto, crear_orden):

    orden = crear_orden

    producto = crear_producto

    detalle_orden = crear_detalle_orden_con_parametros(orden, 2, producto.precio, producto)

    return detalle_orden


@pytest.fixture
def crear_detalles_orden(crear_productos, crear_orden):

    orden = crear_orden

    producto1, producto2, producto3 = crear_productos

    detalle_orden1 = crear_detalle_orden_con_parametros(orden, 10, producto1.precio, producto1)

    detalle_orden2 = crear_detalle_orden_con_parametros(orden, 5, producto3.precio, producto3)

    return detalle_orden1, detalle_orden2, orden

@pytest.fixture
def crear_ordenes_con_detalles(crear_ordenes, crear_productos):

    orden1, orden2 = crear_ordenes

    producto1, producto2, producto3 = crear_productos

    detalle_orden1 = crear_detalle_orden_con_parametros(orden1, 10, producto1.precio, producto1)
    detalle_orden2 = crear_detalle_orden_con_parametros(orden1, 5, producto3.precio, producto3)
    detalle_orden3 = crear_detalle_orden_con_parametros(orden2, 3, producto2.precio, producto2)

    producto1.stock -= 10
    producto3.stock -= 5
    producto2.stock -= 3
    producto1.save()
    producto2.save()
    producto3.save()

    return orden1, detalle_orden1, detalle_orden2, orden2, detalle_orden3, producto1, producto2, producto3







