import pytest
from rest_framework import status


@pytest.mark.django_db
class TestLogin:
    url = '/core/login'

    def test_invalid_credentials(self, client):
        response = client.post(path=self.url, data={
            'username': "random_user",
            'password': "random_user_123"
        })

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {'detail': 'Incorrect authentication credentials.'}

    def test_user_is_inactive(self, client, faker, user_factory):
        password = faker.password()
        user = user_factory.create(password=password, is_active=False)
        response = client.post(path=self.url, data={
            'username': user.username,
            'password': password
        })

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {'detail': 'Incorrect authentication credentials.'}

    def test_login_is_success(self, client, faker, user_factory):
        password = faker.password()
        user = user_factory.create(password=password)
        response = client.post(path=self.url, data={
            'username': user.username,
            'password': password
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            'username': user.username,
            'first_name': None,
            'last_name': None,
            'email': user.email
        }
