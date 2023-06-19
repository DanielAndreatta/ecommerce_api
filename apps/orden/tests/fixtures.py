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
def crear_ordenes():

    orden1 = crear_orden_con_parametros('2023-06-12')

    orden2 = crear_orden_con_parametros('2020-05-11')

    return orden1, orden2


@pytest.fixture
def crear_orden():

    fecha_hora = datetime.strptime('2023-06-12', '%Y-%m-%d')
    orden = crear_orden_con_parametros(fecha_hora)

    return orden


@pytest.fixture
def crear_detalles_orden(crear_productos, crear_orden):

    orden = crear_orden

    producto1, producto2, producto3 = crear_productos

    detalle_orden1 = crear_detalle_orden_con_parametros(orden, 10, producto1.precio, producto1)

    detalle_orden2 = crear_detalle_orden_con_parametros(orden, 5, producto3.precio, producto3)

    return detalle_orden1, detalle_orden2


@pytest.fixture
def crear_detalle_orden(crear_productos, crear_orden):

    orden = crear_orden

    producto1, producto2, producto3 = crear_productos

    detalle_orden = crear_detalle_orden_con_parametros(orden, 2, producto2.precio, producto2)

    return detalle_orden





