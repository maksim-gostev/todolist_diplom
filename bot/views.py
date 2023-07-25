from typing import Any

from rest_framework import generics, permissions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework.response import Response

from bot.models import TgUser
from bot.serializer import TgUserSerializer
from bot.tg.client import TgClient


# Create your views here.
class VerifyUserView(generics.GenericAPIView):
    """
    Верифицируйте пользователя telegram на сайте
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TgUserSerializer

    def patch(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Получите проверочный код и обновите пользователя в базе данных
        :param request:
        :param args:
        :param kwargs:
        :return: response
        """
        serializer: TgUserSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            tg_user: TgUser = TgUser.objects.get(
                verification_code=serializer.validated_data.get('verification_code')
            )
        except TgUser.DoesNotExist:
            raise AuthenticationFailed

        tg_user.user = request.user
        tg_user.save()

        TgClient().send_message(chat_id=tg_user.chat_id, text='Bot verificated')

        return Response(TgUserSerializer(tg_user).data)
