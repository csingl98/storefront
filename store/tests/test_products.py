from rest_framework import status
from django.contrib.auth.models import User
import pytest
from model_bakery import baker
from store.models import Collection

PRODUCTS_ENDPOINT = "/store/products"


@pytest.fixture
def create_product(api_client):
    def do_create_product(product):
        return api_client.post(PRODUCTS_ENDPOINT, product)

    return do_create_product


@pytest.mark.django_db
class TestCreateProduct:
    def test_if_user_is_anonymous_returns_401(self, create_product):
        response = create_product({"title": "a"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestRetrieveProduct:
    pass
