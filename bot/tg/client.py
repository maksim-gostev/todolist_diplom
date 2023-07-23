import logging
from pydantic import ValidationError

from bot.tg.schemas import GetUpdatesResponse, SendMessageResponse
from django.conf import settings
import requests

logger = logging.getLogger(__name__)


class TgClientError(Exception):
    ...


class TgClient:
    def __init__(self, token: str | None = None):
        self.__token = token if token else settings.BOT_TOKEN
        self.__url = f'https://api.telegram.org/bot{self.__token}/'

    def __get_url(self, method: str) -> str:
        return f'{self.__url}{method}'

    def get_updates(self, offset: int = 0, timeout: int = 60, **kwargs) -> GetUpdatesResponse:
        """
        Получайте обновления от telegram-бота
        :параметра offset: смещение
        :параметр timeout: тайм-аут
        :возврат: return
        """
        data = self._get('getUpdates', offset=offset, timeout=timeout, **kwargs)
        return self.__serialize_tg_response(GetUpdatesResponse, data)

    def send_message(self, chat_id: int, text: str, **kwargs) -> SendMessageResponse:
        data = self._get('sendMessage', chat_id=chat_id, text=text, **kwargs)
        return self.__serialize_tg_response(SendMessageResponse, data)

    def _get(self, method: str, **params) -> dict:
        url = self.__get_url(method)
        params.setdefault('timeout', 60)
        response = requests.get(url, params=params)
        if not response.ok:
            logger.warning('Неверный код состояния %d из команды %s', response.status_code, method)
            raise TgClientError
        return response.json()

    @staticmethod
    def __serialize_tg_response(serializer_clas, data):
        try:
            return serializer_clas(**data)
        except ValidationError:
            logger.error('Не удалось сериализовать ответ telegram: %s', data)
            raise TgClientError
