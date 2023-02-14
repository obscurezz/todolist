import datetime

import pytest
import pytz
from rest_framework import status
from rest_framework.fields import DateTimeField

from core.models import User
from goals.models import GoalCategory, Goal


@pytest.mark.django_db
class TestGoalViews:

    def test_goal_create(self, auth_client, faker, goal_category: GoalCategory, goal_factory):
        goal: Goal = goal_factory.build(pk=1,
                                        created=datetime.datetime.now(pytz.utc),
                                        updated=datetime.datetime.now(pytz.utc),
                                        description=faker.text(),
                                        category=goal_category)

        response = auth_client.post(path='/goals/goal/create', data={
            'title': goal.title,
            'category': goal.category.pk,
            'description': goal.description
        }, format='json')

        expected_response = {
            'id': goal.pk,
            'category': goal.category.pk,
            'created': DateTimeField().to_representation(goal.created),
            'updated': DateTimeField().to_representation(goal.updated),
            'title': goal.title,
            'description': goal.description,
            'due_date': DateTimeField().to_representation(goal.due_date),
            'status': goal.status,
            'priority': goal.priority
        }

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == expected_response

    def test_goal_create_not_authenticated(self, client, goal):
        response = client.post(path='/goals/goal/create', data={
            'title': goal.title,
            'board': goal.category.pk
        })

        expected_response = {'detail': 'Authentication credentials were not provided.'}

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == expected_response

    def test_goal_list(self, auth_client, faker, user: User, goal_category: GoalCategory, goal_factory):
        goal_list: list[Goal] = goal_factory.create_batch(1, user=user, category=goal_category,
                                                          description=faker.text())
        response = auth_client.get(path='/goals/goal/list')

        expected_response = [{
            'id': goal_list[i].pk,
            'category': goal_list[i].category.pk,
            'created': DateTimeField().to_representation(goal_list[i].created),
            'updated': DateTimeField().to_representation(goal_list[i].updated),
            'title': goal_list[i].title,
            'description': goal_list[i].description,
            'due_date': DateTimeField().to_representation(goal_list[i].due_date),
            'status': 1,
            'priority': 2,
            'user': user.pk
        } for i in range(len(goal_list))]

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response

    def test_goal_list_not_authenticated(self, client, faker, user: User, goal_category: GoalCategory, goal_factory):
        goal_factory.create_batch(1, user=user, category=goal_category, description=faker.text())
        response = client.get(path='/goals/goal/list')

        expected_response = {'detail': 'Authentication credentials were not provided.'}

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == expected_response

    def test_goal_get(self, auth_client, faker, user: User, goal_category: GoalCategory, goal_factory):
        goal: Goal = goal_factory.create(user=user, category=goal_category, description=faker.text())
        response = auth_client.get(path=f'/goals/goal/{goal.pk}')

        expected_response = {
            'id': goal.pk,
            'category': goal.category.pk,
            'created': DateTimeField().to_representation(goal.created),
            'updated': DateTimeField().to_representation(goal.updated),
            'title': goal.title,
            'description': goal.description,
            'due_date': DateTimeField().to_representation(goal.due_date),
            'status': 1,
            'priority': 2,
            'user': user.pk
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response

    def test_goal_get_not_authenticated(self, client, faker, user: User, goal_category: GoalCategory, goal_factory):
        goal: Goal = goal_factory.create(user=user, category=goal_category, description=faker.text())
        response = client.get(path=f'/goals/goal/{goal.pk}')

        expected_response = {'detail': 'Authentication credentials were not provided.'}

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == expected_response

    def test_goal_update(self, auth_client, faker, user: User, goal_category: GoalCategory, goal_factory):
        goal: Goal = goal_factory.create(user=user, category=goal_category, description=faker.text())
        new_title = faker.company()
        new_description = faker.text()
        response = auth_client.put(path=f'/goals/goal/{goal.pk}', data={
            'title': new_title,
            'description': new_description,
            'category': goal.category.pk
        })

        expected_response = {
            'id': goal.pk,
            'category': goal.category.pk,
            'created': DateTimeField().to_representation(goal.created),
            'updated': DateTimeField().to_representation(goal.updated),
            'title': new_title,
            'description': new_description,
            'due_date': DateTimeField().to_representation(goal.due_date),
            'status': 1,
            'priority': 2,
            'user': user.pk
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response

    def test_goal_delete(self, auth_client, goal: Goal):
        response = auth_client.delete(path=f'/goals/goal/{goal.pk}')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data is None
