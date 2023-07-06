from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination

from goals.filters import GoalDateFilter
from goals.models import GoalCategory, Goal, GoalComment
from goals.serializers import (GoalCategoryCreateSerializers, GoalCategorySerializers, GoalCreateSerializers,
                               GoalSerializers, GoalCommentCreateSerializers, GoalCommentSerializers)


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
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
        return GoalCategory.objects.select_related('user').filter(user=self.request.user, is_deleted=False)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializers

    def get_queryset(self) -> QuerySet:
        return GoalCategory.objects.select_related('user').filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: GoalCategory) :
        instance.is_deleted = True
        instance.save()
        return instance

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
        return (
            Goal.objects.select_related('user')
                .filter(user=self.request.user, category__is_deleted=False)
                .exclude(status=Goal.Status.archived)
        )

class GoalView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializers

    def get_queryset(self) -> QuerySet:
        return (
            Goal.objects.select_related('user')
                .filter(user=self.request.user, category__is_deleted=False)
                .exclude(status=Goal.Status.archived)
        )

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
        return (
            GoalComment.objects.select_related('user')
            .filter(user=self.request.user)
            .exclude(goal__goals__status=Goal.Status.archived)
        )


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
        return (
            GoalComment.objects.select_related('user')
            .filter(user=self.request.user)
            .exclude(goal__goals__status=Goal.Status.archived)
        )
