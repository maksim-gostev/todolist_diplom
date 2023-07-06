from datetime import datetime
from django.utils import timezone

from rest_framework import serializers
from goals.models import GoalCategory, Goal, GoalComment
from core.serializers import ProfileSerializer


class GoalCategoryCreateSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'


class GoalCategorySerializers(GoalCategoryCreateSerializers):
    user = ProfileSerializer(read_only=True)


class GoalCreateSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'

    def validate_category(self, value: GoalCategory) -> GoalCategory:
        if value.is_deleted:
            raise serializers.ValidationError("не допускается в удаленной категории")

        if value.user != self.context["request"].user:
            raise serializers.ValidationError("не владелец категории")

        return value


    def validated_due_data(self, value: datetime | None) -> datetime | None:
        if value:
            if value < timezone.now().date():
                raise serializers.ValidationError('Дата в прошлом')
            return value


class GoalSerializers(GoalCreateSerializers):
    user = ProfileSerializer(read_only=True)


class GoalCommentCreateSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'

    def validate_goal(self, value: Goal) -> Goal:
        if value.status == Goal.Status.archived:
            raise serializers.ValidationError("не допускается в удаленной цели")

        if value.user != self.context["request"].user:
            raise serializers.ValidationError("не владелец категории")

        return value


class GoalCommentSerializers(GoalCommentCreateSerializers):
    user = ProfileSerializer(read_only=True)
    goal = serializers.PrimaryKeyRelatedField(read_only=True)
