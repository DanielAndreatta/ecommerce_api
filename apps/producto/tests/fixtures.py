import pytest
from apps.producto.models import Producto


def crear_producto(nombre, precio, stock):
    producto = Producto.objects.create(
        nombre=nombre,
        precio=precio,
        stock=stock
    )
    return producto


@pytest.fixture
def crear_productos():
    producto1 = crear_producto('Lapicera', '300', 50)

    producto2 = crear_producto('Cuaderno', '1500', 10)

    producto3 = crear_producto('Regla', '800', 20)

    return producto1, producto2, producto3