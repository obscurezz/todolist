from django.db import transaction
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView

from goals.filters import GoalDateFilter, CommentGoalFilter, CategoryBoardFilter
from goals.models import Goal, GoalCategory, GoalComment, Board
from goals.permissions import BoardPermissions, CategoryPermissions, GoalPermissions, \
    CommentPermissions
from goals.serializers import GoalCreateSerializer, GoalSerializer, GoalCategoryCreateSerializer, \
    GoalCategorySerializer, GoalCommentCreateSerializer, GoalCommentSerializer, BoardCreateSerializer, BoardSerializer, \
    BoardListSerializer


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = CategoryBoardFilter
    ordering_fields = ["title", "created"]
    ordering = ["-created"]
    search_fields = ["title"]

    def get_queryset(self):
        return GoalCategory.objects.filter(board__participants__user=self.request.user, is_deleted=False)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [CategoryPermissions]

    def get_queryset(self):
        return GoalCategory.objects.filter(board__participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        Goal.objects.filter(category=instance.id).update(status=4)
        return instance


class GoalCreateView(CreateAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title", "description"]

    def get_queryset(self):
        category_set = GoalCategory.objects.filter(board__participants__user=self.request.user, is_deleted=False)

        return Goal.objects.filter(
            Q(category__in=category_set) & ~Q(status=Goal.Status.archived) & Q(category__is_deleted=False))


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    permission_classes = [GoalPermissions]
    serializer_class = GoalSerializer

    def get_queryset(self):
        category_set = GoalCategory.objects.filter(board__participants__user=self.request.user, is_deleted=False)

        return Goal.objects.filter(
            Q(category__in=category_set) & ~Q(status=Goal.Status.archived) & Q(category__is_deleted=False))

    def perform_destroy(self, instance):
        instance.status = 4
        instance.save()
        return instance


class GoalCommentCreateView(CreateAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView(ListAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_class = CommentGoalFilter
    filterset_fields = ["goal"]
    ordering_fields = ["created"]
    ordering = ["-created"]
    search_fields = ["goal"]

    def get_queryset(self):
        category_set = GoalCategory.objects.filter(board__participants__user=self.request.user, is_deleted=False)

        return GoalComment.objects.filter(goal__category__in=category_set)


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    permission_classes = [CommentPermissions]
    serializer_class = GoalCommentSerializer

    def get_queryset(self):
        category_set = GoalCategory.objects.filter(board__participants__user=self.request.user, is_deleted=False)

        return GoalComment.objects.filter(goal__category__in=category_set)


class BoardCreateView(CreateAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardCreateSerializer


class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated, BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=Goal.Status.archived)

        return instance


class BoardListView(ListAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated, BoardPermissions]
    serializer_class = BoardListSerializer
    filter_backends = [
        filters.OrderingFilter,
    ]
    ordering = ['-title']

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)
