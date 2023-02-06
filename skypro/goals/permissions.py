from rest_framework import permissions

from goals.models import Board, BoardParticipant, GoalCategory, Goal, GoalComment


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user.id


class BoardPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj: Board):
        check: dict = {'user': request.user, 'board': obj}
        if request.method not in permissions.SAFE_METHODS:
            check['role'] = BoardParticipant.Role.owner

        return BoardParticipant.objects.filter(**check).exists()


class CategoryPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj: GoalCategory):
        check: dict = {'user': request.user, 'board': obj.board}
        if request.method not in permissions.SAFE_METHODS:
            check['role__in'] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]

        return BoardParticipant.objects.filter(**check).exists()


class GoalPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj: Goal):
        check: dict = {'user': request.user, 'board': obj.category.board}
        if request.method not in permissions.SAFE_METHODS:
            check['role__in'] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]

        return BoardParticipant.objects.filter(**check).exists()


class CommentPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj: GoalComment):
        return any((request.method in permissions.SAFE_METHODS, obj.user == request.user.id))
