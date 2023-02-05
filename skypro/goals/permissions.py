from rest_framework import permissions

from goals.models import Board, BoardParticipant, GoalCategory, Goal, GoalComment


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user.id


class BoardPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj: Board):
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board=obj).exists()
        return BoardParticipant.objects.filter(user=request.user, board=obj, role=BoardParticipant.Role.owner).exists()


class CategoryPermissions(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj: GoalCategory):

        if not request.user.is_authenticated:
            return False

        # if method is not safe (e.g. 'PUT', 'DELETE') check whether the user is owner or writer
        if request.method not in permissions.SAFE_METHODS:
            return GoalCategory.objects.filter(board__participants__user=request.user,
                                               board__participants__role__in=[1, 2],
                                               user__goalcategory=obj).exists()
        return True


class GoalPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Goal):

        if not request.user.is_authenticated:
            return False

        if request.method not in permissions.SAFE_METHODS:
            return GoalCategory.objects.filter(board__participants__user=request.user,
                                               board__participants__role__in=[1, 2],
                                               user__goal=obj).exists()
        return True


class CommentPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: GoalComment):

        if not request.user.is_authenticated:
            return False

        if request.method not in permissions.SAFE_METHODS:
            return GoalCategory.objects.filter(board__participants__user=request.user,
                                               board__participants__role__in=[1, 2],
                                               goals__goalcomment=obj).exists()
        return True
