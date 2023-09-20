from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
import pytest
from model_bakery import baker
from store.models import Collection


@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collection/', collection)
    return do_create_collection


@pytest.fixture
def authenticate_user(api_client):
    def do_authenticate_user(is_staff=False):
        api_client.force_authenticate(user=User(is_staff=is_staff))
    return do_authenticate_user


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_return_401(self, create_collection):
        # AAA (Arrange,Act,Assert)
        # Arrange

        # ACT
        response = create_collection({
            'title': 'a'
        })
        # assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_return_403(self, create_collection, authenticate_user):
        # AAA (Arrange,Act,Assert)
        # Arrange
        authenticate_user()

        # ACT
        response = create_collection({
            'title': 'a'
        })
        # assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_return_400(self, create_collection, authenticate_user):
        # AAA (Arrange,Act,Assert)
        # Arrange
        authenticate_user(is_staff=True)
        # ACT
        response = create_collection({
            'title': ' '
        })
        # assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_return_201(self, create_collection, authenticate_user):
        # AAA (Arrange,Act,Assert)
        # Arrange
        authenticate_user(is_staff=True)

        # ACT
        response = create_collection({
            'title': 'a'
        })
        # assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestReteriveCollection:
    def test_if_collection_exists_return_200(self, api_client):
        collection = baker.make(Collection)
        # print(collection.__dict__)
        response = api_client.get(f'/store/collection/{collection.id}/')
        assert response.status_code == status.HTTP_200_OK
