from rest_framework import serializers, exceptions

from core.serializers import ProfileSerializer
from goals.models import Goal, GoalCategory, GoalComment


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCategorySerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")
        extra_kwargs = {
            'is_deleted': {'write_only': True}
        }


class GoalCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=GoalCategory.objects.filter(is_deleted=False))
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate_category(self, value: GoalCategory):
        if value.user != self.context["request"].user:
            raise exceptions.PermissionDenied

        return value


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate_category(self, value: GoalCategory):
        if value.user != self.context["request"].user:
            raise exceptions.PermissionDenied

        return value


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    text = serializers.CharField(min_length=1, max_length=4000, allow_blank=False)

    class Meta:
        model = GoalComment
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"
    #
    # def validate_user(self, value):
    #     if value.user != self.context["request"].user:
    #         raise serializers.ValidationError("not owner of commentary")
    #
    #     return value


class GoalCommentSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalComment
        read_only_fields = ("id", "created", "updated", "user", "goal")
        fields = "__all__"
