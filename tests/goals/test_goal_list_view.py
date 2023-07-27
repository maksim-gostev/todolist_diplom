import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response


class TestGoalListView:
    url = reverse('goals:goal-list')

    @pytest.mark.django_db()
    def test_auth_required_list_view(self, client):
        """
        Неавторизованный пользователь получает ошибку авторизации
        """
        response: Response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
