import pytest
from apps.orden.models import DetalleOrden, Orden
from datetime import datetime
from apps.producto.tests.fixtures import crear_productos


def crear_orden(fecha_hora):
    orden, _ = Orden.objects.get_or_create(
        fecha_hora=fecha_hora
    )
    return orden


def crear_detalle_orden(orden, cantidad, precio_unitario, producto):
    detalles_orden, _ = DetalleOrden.objects.get_or_create(
        orden=orden,
        cantidad=cantidad,
        precio_unitario=precio_unitario,
        producto=producto
    )

    return detalles_orden


@pytest.fixture
def crear_ordenes():

    orden1 = crear_orden('2023-06-12')

    orden2 = crear_orden('2020-05-11')

    return orden1, orden2


@pytest.fixture
def crear_ordenes2():

    orden1 = crear_orden('2023-06-12')

    return orden1


@pytest.fixture
def crear_ordenes_y_detalles1(crear_productos):

    orden1 = crear_orden('2023-06-12')

    producto1, producto2, producto3 = crear_productos

    detalles_orden1 = crear_detalle_orden(orden1, 10, producto1.precio, producto1)

    detalles_orden2 = crear_detalle_orden(orden1, 5, producto3.precio, producto3)

    return detalles_orden1, detalles_orden2

@pytest.fixture
def crear_ordenes_y_detalles2(crear_productos):

    orden1 = crear_orden('2023-06-12')

    producto1, producto2, producto3 = crear_productos

    detalles_orden2 = crear_detalle_orden(orden1, 2, producto2.precio, producto2)

    return detalles_orden2


"""
@pytest.fixture
def ordenfixture_con_detalles(crear_ordenes2, crear_productos, cantidad):

    orden1 = crear_ordenes2

    producto1, producto2, producto3 = crear_productos

    data = {
        "orden": orden1.id,
        "cantidad": cantidad,
        "precio_unitario": producto3.precio,
        "producto": producto3.id,
    }

    return data
"""


