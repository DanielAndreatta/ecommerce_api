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

    response = client.put(f'/api/v1/producto/{producto.uuid}/stock/', {'stock': nuevo_stock})

    assert response.status_code == 200

    #Realiza una consulta a la base de datos para obtener los valores más recientes de los campos del objeto y los actualiza en el objeto en memoria.
    producto.refresh_from_db()

    assert producto.stock == nuevo_stock
