from core.models import User
from goals.models import Goal, GoalCategory, GoalComment, Board, BoardParticipant
import factory.fuzzy


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username: str = factory.Faker('user_name')
    email: str = factory.Faker('email')
    password: str = 'test_password'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return cls._get_manager(model_class).create_user(*args, **kwargs)


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title: str = factory.fuzzy.FuzzyText(length=8)

    @factory.post_generation
    def set_owner(self, create, user, **kwargs):
        if user:
            BoardParticipant.objects.create(
                board=self,
                user=user,
                role=BoardParticipant.Role.owner
            )


class GoalCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalCategory

    title: str = factory.fuzzy.FuzzyText(length=8)
    user: User = factory.SubFactory(UserFactory)
    board: Board = factory.SubFactory(BoardFactory)


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal

    title: str = factory.fuzzy.FuzzyText(length=8)
    user: User = factory.SubFactory(UserFactory)
    category: GoalCategory = factory.SubFactory(GoalCategoryFactory)


class GoalCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalComment

    text: str = factory.fuzzy.FuzzyText(length=30)
    user: User = factory.SubFactory(UserFactory)
    goal: Goal = factory.SubFactory(GoalFactory)
