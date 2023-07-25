import requests
from django.conf import settings
from requests import Response

from bot.tg.schemas import GetUpdatesResponse, SendMessageResponse


class TgClient:
    """
    Класс взаимодействия с telegram-ботом
    """

    def __init__(self, token: str = settings.BOT_TOKEN) -> None:
        self.token = token

    def get_url(self, method: str) -> str:
        """
        Получить URL-адрес в зависимости от метода
        :param method: telegram method
        :return: url for request
        """
        return f'https://api.telegram.org/bot{self.token}/{method}'

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        """
        Получайте обновления от telegram-бота
        :param offset: offset
        :param timeout: timeout
        :return: response
        """
        response: Response = requests.get(
            self.get_url('getUpdates'), params={'offset': offset, 'timeout': timeout}
        )
        data = response.json()
        return GetUpdatesResponse(**data)

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        """
        Отправить сообщение telegram-боту
        :param chat_id: chat id
        :param text: text message
        :return: response
        """
        response: Response = requests.get(
            self.get_url('sendMessage'), params={'chat_id': chat_id, 'text': text}
        )
        data = response.json()
        return SendMessageResponse(**data)
