import pytest
from rest_framework import status

from core.models import User


@pytest.mark.django_db
class TestSignup:
    url = '/core/signup'

    def test_signup_success(self, client, user_factory):
        user: User = user_factory.build()
        response = client.post(path=self.url, data={
            'username': user.username,
            'first_name': "fake_first",
            'last_name': "fake_last",
            'email': user.email,
            'password': user.password,
            'password_repeat': user.password,
        }, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            'username': user.username,
            'first_name': "fake_first",
            'last_name': "fake_last",
            'email': user.email,
        }

    def test_signup_not_success(self, client, user_factory):
        user: User = user_factory.build()
        response = client.post(path=self.url, data={
            'username': user.username,
            'email': user.email,
            'password': user.password,
            'password_repeat': user.password,
        }, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            "first_name": [
                "This field is required."
            ],
            "last_name": [
                "This field is required."
            ]
        }
