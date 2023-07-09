from typing import Any

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.generics import GenericAPIView

from goals.models import Board, GoalCategory, Goal, GoalComment, BoardParticipant


class BoardPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request: Request, view: GenericAPIView, obj: Board) -> bool:
        _filter = dict[str, Any] = {'user_id': request.user.id, 'board_id': obj.id}
        if request.method not in permissions.SAFE_METHODS:
            _filter['role'] = BoardParticipant.Role.owner
        return BoardParticipant.objects.filter(**_filter).exists()



class GoalCategoryPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request: Request, view: GenericAPIView, obj: GoalCategory) -> bool:
        _filter = dict[str, Any] = {'user_id': request.user.id, 'board_id': obj.board_id}
        if request.method not in permissions.SAFE_METHODS:
            _filter['role'] = BoardParticipant.Role.owner
        return BoardParticipant.objects.filter(**_filter).exists()



class GoalPermission(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: GenericAPIView, obj: Goal) -> bool:
        _filter = dict[str, Any] = {'user_id': request.user.id, 'board_id': obj.category.board_id}
        if request.method not in permissions.SAFE_METHODS:
            _filter['role'] = BoardParticipant.Role.owner
        return BoardParticipant.objects.filter(**_filter).exists()

class GoalCommentPermission(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: GenericAPIView, obj: GoalComment) -> bool:
        _filter = dict[str, Any] = {'user_id': request.user.id, 'board_id': obj.goal.board_id}
        if request.method not in permissions.SAFE_METHODS:
            return obj.user == request.user
        return BoardParticipant.objects.filter(**_filter).exists()
