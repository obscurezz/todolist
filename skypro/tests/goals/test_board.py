import pytest
from rest_framework import status
from rest_framework.fields import DateTimeField
from goals.models import Board
from unittest.mock import ANY


@pytest.mark.django_db
class TestBoardViews:

    def test_board_create(self, auth_client, board: Board):
        response = auth_client.post(path='/goals/board/create', data={
            'title': board.title
        }, format='json')

        expected_response = {
            'id': 2,
            'created': DateTimeField().to_representation(board.created),
            'updated': DateTimeField().to_representation(board.updated),
            'title': board.title,
            'is_deleted': board.is_deleted
        }

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == expected_response

    def test_board_create_not_authenticated(self, client, board: Board):
        response = client.post(path='/goals/board/create', data={
            'title': board.title
        })

        expected_response = {'detail': 'Authentication credentials were not provided.'}

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == expected_response

    def test_board_list(self, auth_client, user, board_factory):
        board_list: list[Board] = board_factory.create_batch(1, set_owner=user)
        response = auth_client.get(path='/goals/board/list')

        expected_response = [{
            'id': board_list[i].pk,
            'created': DateTimeField().to_representation(board_list[i].created),
            'updated': DateTimeField().to_representation(board_list[i].updated),
            'title': board_list[i].title,
            'is_deleted': board_list[i].is_deleted
        } for i in range(len(board_list))]

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response

    def test_board_list_not_authenticated(self, client, user, board_factory):
        board_factory.create_batch(2, set_owner=user)
        response = client.get(path='/goals/board/list')

        expected_response = {'detail': 'Authentication credentials were not provided.'}

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == expected_response

    def test_board_get(self, auth_client, user, board_factory):
        board: Board = board_factory.create(set_owner=user)
        response = auth_client.get(path=f'/goals/board/{board.pk}')

        expected_response = {
            'id': board.pk,
            'created': DateTimeField().to_representation(board.created),
            'updated': DateTimeField().to_representation(board.updated),
            'title': board.title,
            'is_deleted': board.is_deleted,
            'participants': [{'board': board.pk,
                              'created': DateTimeField().to_representation(board.created),
                              'updated': DateTimeField().to_representation(board.updated),
                              'id': ANY,
                              'role': 1,
                              'user': user.username}],
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response

    def test_board_get_not_authenticated(self, client, board: Board):
        response = client.get(path=f'/goals/board/{board.pk}')

        expected_response = {'detail': 'Authentication credentials were not provided.'}

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == expected_response

    def test_board_update(self, auth_client, user, faker, board_factory):
        board: Board = board_factory.create(set_owner=user)
        new_title = faker.text()
        response = auth_client.put(path=f'/goals/board/{board.pk}', data={
            'title': new_title
        })

        expected_response = {
            'id': board.pk,
            'created': DateTimeField().to_representation(board.created),
            'updated': DateTimeField().to_representation(board.updated),
            'title': new_title,
            'is_deleted': board.is_deleted,
            'participants': [{'board': board.pk,
                              'created': DateTimeField().to_representation(board.created),
                              'updated': DateTimeField().to_representation(board.updated),
                              'id': ANY,
                              'role': 1,
                              'user': user.username}],
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response

    def test_board_delete(self, auth_client, board: Board):
        response = auth_client.delete(path=f'/goals/board/{board.pk}')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data is None
