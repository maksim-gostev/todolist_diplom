from django.db.models import QuerySet
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination

from goals.filters import GoalDateFilter
from goals.models import GoalCategory, Goal, GoalComment, BoardParticipant, Board
from goals.permissions import BoardPermissions
from goals.serializers import (GoalCategoryCreateSerializers, GoalCategorySerializers, GoalCreateSerializers,
                               GoalSerializers, GoalCommentCreateSerializers, GoalCommentSerializers,
                               BoardCreateSerializer, BoardSerializer)

class BoardCreateView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardCreateSerializer

    def perform_create(self, serializer: BoardCreateSerializer) -> None:
        with transaction.atomic():
            board = serializer.save()
            BoardParticipant.objects.create(user=self.request.user, board=board)


class BoardListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.OrderingFilter]
    ordering = ['title']

    def get_queryset(self) -> QuerySet:
        return Board.objects.filter(participants__user_id=self.request.user.id).exclude(is_deleted=True)


class BoardView(RetrieveUpdateDestroyAPIView):
    pagination_class = [BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self) -> QuerySet:
        return Board.objects.prefetch_related('participants__user').exclude(is_deleted=True)

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            Board.objects.filter(id=instance.objects).update(is_deleted=True)
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=Goal.Status.archived)


class GoalCategoryCreateView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializers

class GoalCategoryListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializers
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title']
    def get_queryset(self) -> QuerySet:
        return GoalCategory.objects.filter(board__participants__user=self.request.user, is_deleted=False)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializers

    def get_queryset(self) -> QuerySet:
        return GoalCategory.objects.filter(board__participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: GoalCategory) :
        instance.is_deleted = True
        instance.save(update_fields=('is_deleted'))
        instance.goals.update(status=Goal.Status.archived)

class GoalCreateView(CreateAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCreateSerializers


class GoalListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializers
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title', 'description']

    def get_queryset(self) -> QuerySet:
        return Goal.objects.filter(
            category__board__participants__user_id=self.request.user.id ,category__is_deleted=False
        ).exclude(status=Goal.Status.archived)

class GoalView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializers

    def get_queryset(self) -> QuerySet:
        return Goal.objects.filter(
            category__board__participants__user_id=self.request.user.id ,category__is_deleted=False
        ).exclude(status=Goal.Status.archived)

    def perform_destroy(self, instance: Goal):
        instance.status = Goal.Status.archived
        instance.save(update_fields=('status',))


class GoalCommentCreateView(CreateAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentCreateSerializers


class GoalCommentListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentSerializers
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]

    ordering = ['-created']
    ordering_fields = ['title', 'description']
    filterset_fields = ['goal']

    def get_queryset(self) -> QuerySet:
        return GoalComment.objects.filter(goal__category__board__participants__user_id=self.request.user.id
                                          ).exclude(goal__goals__status=Goal.Status.archived)


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentSerializers
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]

    ordering = ['-created']
    ordering_fields = ['title', 'description']
    filterset_fields = ['goal']

    def get_queryset(self) -> QuerySet:
        return GoalComment.objects.filter(goal__category__board__participants__user_id=self.request.user.id
                                          ).exclude(goal__goals__status=Goal.Status.archived)
