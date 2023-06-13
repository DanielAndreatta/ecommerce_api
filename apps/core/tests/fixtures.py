import pytest
from django.contrib.auth import get_user_model


User = get_user_model()


def create_user(username, first_name='Admin', last_name='Root', email=None, *, is_active=True):
    user, created = User.objects.get_or_create(
        username=username,
        email='{}@root.com'.format(username) if email is None else email,
        defaults=dict(
            first_name=first_name,
            last_name=last_name,
            password='password',
            is_active=is_active
        )
    )

    return user


@pytest.fixture(scope='session')
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def get_default_test_user():
    test_user = create_user(username='test_user', first_name='Test', last_name='User', email='test@user')
    return test_user