import pytest
from apps.producto.models import Producto
from apps.core.tests.fixtures import api_client, get_default_test_user
from apps.producto.tests.fixtures import crear_producto


#Inciso 6 (verificar que al ejecutar el endpoint de modificación del stock de un producto, actualiza correctamente dicho stock)
@pytest.mark.django_db
def test_api_actualizar_stock_producto(api_client, get_default_test_user, crear_producto):

    client = api_client
    client.force_authenticate(user=get_default_test_user)

    producto = crear_producto
    nuevo_stock = 15

    # El stock del producto antes del cambio, es igual a 50
    assert producto.stock == 50

    response = client.put(f'/api/v1/producto/{producto.uuid}/stock/', {'stock': nuevo_stock})

    assert response.status_code == 200

    #Realiza una consulta a la base de datos para obtener los valores más recientes de los campos del objeto y los actualiza en el objeto en memoria.
    producto.refresh_from_db()
    # Nuevo stock tiene que ser igual a 15
    assert producto.stock == nuevo_stock


#Test unitario para verificar que se creo el producto correctamente
@pytest.mark.django_db
def test_crear_producto():

    producto = Producto(nombre="Cuaderno", precio=100, stock=50)

    assert producto is not None
    assert producto.nombre == "Cuaderno"
    assert producto.precio == 100
    assert producto.stock == 50


#Test unitario para verificar que se suma el stock del producto
@pytest.mark.django_db
def test_sumar_stock_producto():

    producto = Producto(nombre="Cuaderno", precio=100, stock=50)

    nuevo_stock = 15

    producto.sumar_stock(nuevo_stock)

    # Verificamos que el stock del producto se haya actualizado correctamente
    assert producto.stock == 65


#Test unitario para verificar que se resta el stock del producto
@pytest.mark.django_db
def test_restar_stock_producto():

    producto = Producto(nombre="Cuaderno", precio=100, stock=50)

    nuevo_stock = 15

    producto.restar_stock(nuevo_stock)

    # Verificamos que el stock del producto se haya actualizado correctamente
    assert producto.stock == 35


#Test unitario para verificar que se actualice el stock del producto
@pytest.mark.django_db
def test_actualizar_stock_producto():

    producto = Producto(nombre="Cuaderno", precio=100, stock=50)

    nuevo_stock = 70

    producto.reestablecer_stock(nuevo_stock)

    # Verificamos que el stock del producto se haya actualizado correctamente
    assert producto.stock == 70

