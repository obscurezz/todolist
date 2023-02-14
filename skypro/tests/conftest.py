import pytest
from tests.factories import UserFactory, BoardFactory, GoalCategoryFactory, GoalFactory, GoalCommentFactory
from pytest_factoryboy import register
from goals.models import Board, Goal, GoalCategory


pytest_plugins = 'tests.fixtures'


register(UserFactory)
register(BoardFactory)
register(GoalCategoryFactory)
register(GoalFactory)
register(GoalCommentFactory)


@pytest.fixture()
def board(user) -> Board:
    return BoardFactory.create(set_owner=user)


@pytest.fixture()
def category(user, board) -> GoalCategory:
    return GoalCategoryFactory.create(board=board, user=user)


@pytest.fixture()
def goal(user, board, category) -> Goal:
    return GoalFactory.create(category=category, user=user)
