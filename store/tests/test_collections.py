from rest_framework import status
from django.contrib.auth.models import User
import pytest
from model_bakery import baker
from store.models import Collection

@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection)
    return do_create_collection

@pytest.mark.django_db
class TestCreateCollection:

    def test_if_user_is_anonymous_returns_401(self, create_collection):
        ### Arrange: Set up database or underlying state 

        #Act: Send Request to Server
        response = create_collection({'title': 'a'})

        #Assert: Check if behavior matches what we expect
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_if_user_is_not_admin_returns_403(self, authenticate_user, create_collection):  
        authenticate_user()
        
        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN    
   
    def test_if_data_is_invalid_return_400(self, authenticate_user, create_collection):
        authenticate_user(is_staff=True)
        
        response = create_collection({'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None   

    def test_if_data_is_valid_return_201(self, authenticate_user, create_collection):
        authenticate_user(is_staff=True)
        
        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0

@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exists_returns_200(self, api_client):
        collection = baker.make(Collection)

        response = api_client.get(f'/store/collections/{collection.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id' : collection.id,
            'title' : collection.title,
            'products_count' : 0
        }
