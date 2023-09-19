from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
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

    def test_if_user_is_not_admin_return_403(self):
        # AAA (Arrange,Act,Assert)
        # Arrange
        client = APIClient()
        # ACT
        client.force_authenticate(user={})
        response = client.post('/store/collection/', {
            'title': 'a'
        })
        # assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_return_400(self):
        # AAA (Arrange,Act,Assert)
        # Arrange
        client = APIClient()
        # ACT
        client.force_authenticate(user=User(is_staff=True))
        response = client.post('/store/collection/', {
            'title': ' '
        })
        # assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_return_201(self):
        # AAA (Arrange,Act,Assert)
        # Arrange
        client = APIClient()
        # ACT
        client.force_authenticate(user=User(is_staff=True))
        response = client.post('/store/collection/', {
            'title': 'a'
        })
        # assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0
