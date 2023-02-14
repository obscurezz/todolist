import datetime

import pytest
import pytz
from rest_framework import status
from rest_framework.fields import DateTimeField

from core.models import User
from goals.models import GoalCategory, Board


@pytest.mark.django_db
class TestCategoryViews:

    def test_category_create(self, auth_client, goal_category_factory, board: Board):
        goal_category: GoalCategory = goal_category_factory.build(pk=1,
                                                                  created=datetime.datetime.now(pytz.utc),
                                                                  updated=datetime.datetime.now(pytz.utc),
                                                                  board=board)

        response = auth_client.post(path='/goals/goal_category/create', data={
            'title': goal_category.title,
            'board': goal_category.board.pk
        }, format='json')

        expected_response = {
            'id': goal_category.pk,
            'created': DateTimeField().to_representation(goal_category.created),
            'updated': DateTimeField().to_representation(goal_category.updated),
            'title': goal_category.title,
            'is_deleted': goal_category.is_deleted,
            'board': board.pk
        }

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == expected_response

    def test_category_create_not_authenticated(self, client, goal_category):
        response = client.post(path='/goals/goal_category/create', data={
            'title': goal_category.title,
            'board': goal_category.board.pk
        })

        expected_response = {'detail': 'Authentication credentials were not provided.'}

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == expected_response

    def test_category_list(self, auth_client, user: User, board: Board, goal_category_factory):
        goal_category_list: list[GoalCategory] = goal_category_factory.create_batch(1, user=user, board=board)
        response = auth_client.get(path='/goals/goal_category/list')

        expected_response = [{
            'id': goal_category_list[i].pk,
            'user': {
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            },
            'created': DateTimeField().to_representation(goal_category_list[i].created),
            'updated': DateTimeField().to_representation(goal_category_list[i].updated),
            'title': goal_category_list[i].title,
            'board': board.pk
        } for i in range(len(goal_category_list))]

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response

    def test_category_list_not_authenticated(self, client, user: User, board: Board, goal_category_factory):
        goal_category_factory.create_batch(1, user=user, board=board)
        response = client.get(path='/goals/goal_category/list')

        expected_response = {'detail': 'Authentication credentials were not provided.'}

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == expected_response

    def test_category_get(self, auth_client, user: User, board: Board, goal_category_factory):
        goal_category: GoalCategory = goal_category_factory.create(user=user, board=board)
        response = auth_client.get(path=f'/goals/goal_category/{goal_category.pk}')

        expected_response = {
            'id': goal_category.pk,
            'user': {
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            },
            'created': DateTimeField().to_representation(goal_category.created),
            'updated': DateTimeField().to_representation(goal_category.updated),
            'title': goal_category.title,
            'board': board.pk
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response

    def test_category_get_not_authenticated(self, client, user: User, board: Board, goal_category_factory):
        goal_category: GoalCategory = goal_category_factory.create(user=user, board=board)
        response = client.get(path=f'/goals/goal_category/{goal_category.pk}')

        expected_response = {'detail': 'Authentication credentials were not provided.'}

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == expected_response

    def test_category_update(self, auth_client, faker, user: User, board: Board, goal_category_factory):
        goal_category: GoalCategory = goal_category_factory.create(user=user, board=board)
        new_title = faker.company()
        response = auth_client.put(path=f'/goals/goal_category/{goal_category.pk}', data={
            'title': new_title,
            'board': board.pk
        })

        expected_response = {
            'id': goal_category.pk,
            'user': {
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            },
            'created': DateTimeField().to_representation(goal_category.created),
            'updated': DateTimeField().to_representation(goal_category.updated),
            'title': new_title,
            'board': board.pk
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response

    def test_category_update_not_successful(self, auth_client, faker, user: User, board: Board, goal_category_factory):
        goal_category: GoalCategory = goal_category_factory.create(user=user, board=board)
        new_title = faker.company()
        response = auth_client.put(path=f'/goals/goal_category/{goal_category.pk}', data={
            'title': new_title
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'board': ['This field is required.']}

    def test_category_delete(self, auth_client, goal_category):
        response = auth_client.delete(path=f'/goals/goal_category/{goal_category.pk}')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data is None
