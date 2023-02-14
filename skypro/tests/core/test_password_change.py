import pytest
from rest_framework import status

from core.models import User


@pytest.mark.django_db
class TestPasswordUpdate:
    url = '/core/update_password'

    def test_password_update_success(self, auth_client, faker, user_factory):
        new_password = faker.password()

        user: User = user_factory.build()
        response = auth_client.put(path=self.url, data={
            'old_password': user.password,
            'new_password': new_password
        })

        assert response.status_code == status.HTTP_200_OK

    def test_password_update_not_success(self, auth_client, faker, user_factory):
        user: User = user_factory.build()
        response = auth_client.put(path=self.url, data={
            'old_password': user.password
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
