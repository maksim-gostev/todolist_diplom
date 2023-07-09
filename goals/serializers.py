from datetime import datetime

from django.db import transaction
from django.utils import timezone

from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.request import Request
from core.models import User
from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant
from core.serializers import ProfileSerializer


class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated")
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data.pop("user")
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user, board=board, role=BoardParticipant.Role.owner
        )
        return board


class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        required=True, choices=BoardParticipant.editable_roles
    )
    user = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board")


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")

    def update(self, instance: Board, validated_data: dict) -> Board:
        requests: Request = self.context["request"]
        with transaction.atomic():
            BoardParticipant.objects.filter(board=instance).exclude(user=requests.user).delete()
            new_participant = []
            for participants in validated_data('participants', []):
                new_participant.append(
                    BoardParticipant(user=participants['user'], role=participants['role'], board=instance)
                )
            BoardParticipant.objects.bulk_create(new_participant, ignore_conflicts=True)

            if title := validated_data.get('title'):
                instance.title = title
            instance.save()
        return instance



class GoalCategoryCreateSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'


    def validate_board(self, board: Board) -> Board:
        if board.is_deleted:
            raise ValidationError('Доска удалена')
        if not BoardParticipant.objects.filter(
            user_id=self.context["request"].user.id,
            board_id=board.id,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        ).exists():
            raise PermissionDenied


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
            raise ValidationError("не допускается в удаленной категории")

        if not BoardParticipant.objects.filter(
            user_id=self.context["request"].user.id,
            board_id=value.board.id,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        ).exists():
            raise PermissionDenied

        return value


    def validated_due_data(self, value: datetime | None) -> datetime | None:
        if value:
            if value < timezone.now().date():
                raise ValidationError('Дата в прошлом')
            return value


class GoalSerializers(GoalCreateSerializers):
    user = ProfileSerializer(read_only=True)

    def validate_category(self, value: GoalCategory) -> GoalCategory:
        if value.is_deleted:
            raise ValidationError('Категория удалена')


class GoalCommentCreateSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'

    def validate_goal(self, value: Goal) -> Goal:
        if value.status == Goal.Status.archived:
            raise ValidationError("не допускается в удаленной цели")

        if not BoardParticipant.objects.filter(
            user_id=self.context["request"].user.id,
            board_id=value.category.board_id,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        ).exists():
            raise PermissionDenied
        return value


class GoalCommentSerializers(GoalCommentCreateSerializers):
    user = ProfileSerializer(read_only=True)
    goal = serializers.PrimaryKeyRelatedField(read_only=True)


    def validate_goal(self, value: Goal) -> Goal:
        if value.status == Goal.Status.archived:
            raise ValidationError('Цель не найдена')
        if self.context["request"].user.id != value.user.id:
            raise PermissionDenied
        return value



