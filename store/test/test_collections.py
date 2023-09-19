from rest_framework.test import APIClient
from rest_framework import status
import pytest


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_return_401(self):
        # AAA (Arrange,Act,Assert)
        # Arrange
        client = APIClient()
        # ACT
        response = client.post('/store/collection/', {
            'title': 'a'
        })
        # assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
