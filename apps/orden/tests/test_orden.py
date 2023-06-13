import pytest
from apps.core.tests.fixtures import api_client, get_default_test_user
from apps.orden.tests.fixtures import crear_ordenes


@pytest.mark.django_db
def test_api_lista_ordenes(api_client, get_default_test_user, crear_ordenes):

    client = api_client

    client.force_authenticate(user=get_default_test_user)

    response = client.get(f'/api/v1/orden/')

    assert response.status_code == 200

    json_data = response.json()

    assert len(json_data) == 2

    assert json_data[0]['fecha_hora'] == '2023-06-12T00:00:00Z'

    assert json_data[1]['fecha_hora'] == '2020-05-11T00:00:00Z'

