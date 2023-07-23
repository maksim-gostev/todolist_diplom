from typing import Any

from django.core.management import BaseCommand
from django.db.models import QuerySet

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.schemas import Message, GetUpdatesResponse, SendMessageResponse
from goals.models import Goal, GoalCategory


class Command(BaseCommand):
    """ """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.tg_client: TgClient = TgClient()
        self.states: dict = {}

    def handle(self, *args: Any, **options: Any) -> None:
        """
        Получение сообщения
        :param args:
        :param options:
        :return: message
        """
        offset: int = 0
        while True:
            res: GetUpdatesResponse = self.tg_client.get_updates(offset=offset, allowed_updates='message')
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)

    def handle_message(self, message: Message) -> None:
        """
        Обрабатывает  сообщения от авторизованного или неавторизованного пользователя, возвращает сообщения
        :param message: сообщение пользователя
        :return: Answer from bot
        """
        tg_user, created = TgUser.objects.get_or_create(chat_id=message.chat.id,
                                                        defaults={'username': message.chat.username})

        if not tg_user.is_verified:
            tg_user.update_verification_cod()
            self.tg_client.send_message(message.chat.id, f'Код подтверждения: {tg_user.verification_code}')
        else:
            self.handler_authorized_user(tg_user=tg_user, message=message)

    def handler_authorized_user(self, tg_user: TgUser, message: Message) -> None:
        """
        Возвращает ответы, которые зависят от команд авторизованного пользователя
        :param tg_user: telegram user
        :param message: user message
        :return: Answer from bot
        """
        commands: list = ['/goals', '/create', '/cancel']
        create_chat: dict | None = self.states.get(message.chat.id, None)

        if message.text == '/cancel':
            self.states.pop(message.chat.id, None)
            create_chat = None
            self.tg_client.send_message(chat_id=message.chat.id, text='Операция была отменена')

        if message.text in commands and not create_chat:
            if message.text == '/goals':
                qs = Goal.objects.filter(
                    category__is_deleted=False, category__board__participants__user_id=tg_user.user.id
                ).exclude(status=Goal.Status.archived)
                goals = [f'{goal.id} - {goal.title}' for goal in qs]
                self.tg_client.send_message(chat_id=message.chat.id, text='Никаких целей' if not goals else '\n'.join(goals))

            if message.text == '/create':
                categories_qs = GoalCategory.objects.filter(
                    board__participants__user_id=tg_user.user.id, is_deleted=False
                )

                categories = []
                categories_id = []
                for category in categories_qs:
                    categories.append(f'{category.id} - {category.title}')
                    categories_id.append(str(category.id))

                self.tg_client.send_message(
                    chat_id=message.chat.id, text=f'Выберите номер категории:\n' + '\n'.join(categories)
                )
                self.states[message.chat.id] = {
                    'categories': categories,
                    'categories_id': categories_id,
                    'category_id': '',
                    'goal_title': '',
                    'stage': 1,
                }
        if message.text not in commands and create_chat:
            if create_chat['stage'] == 2:
                Goal.objects.create(
                    user_id=tg_user.user.id,
                    category_id=int(self.states[message.chat.id]['category_id']),
                    title=message.text,
                )
                self.tg_client.send_message(chat_id=message.chat.id, text='Сохранение цели')
                self.states.pop(message.chat.id, None)

            elif create_chat['stage'] == 1:
                if message.text in create_chat.get('categories_id', []):
                    self.tg_client.send_message(chat_id=message.chat.id, text='Введите название цели')
                    self.states[message.chat.id] = {'category_id': message.text, 'stage': 2}
                else:
                    self.tg_client.send_message(
                        chat_id=message.chat.id,
                        text='Введите правильный номер категории\n' + '\n'.join(create_chat.get('categories', [])),
                    )

        if message.text not in commands and not create_chat:
            self.tg_client.send_message(chat_id=message.chat.id, text=f'Неизвестная команда!')

    def _get_goals(self, message: Message, tg_user: TgUser) -> SendMessageResponse:
        """
        Возвращает цели пользователя или "Нет целей", если цели не существуют
        :param message: user message
        :param tg_user: telegram user
        :return: Message with user goals
        """
        query_set: QuerySet = (
            Goal.objects.select_related('user')
            .filter(user_id=tg_user.user.id, category__is_deleted=False)
            .exclude(status=Goal.Status.archived)
        )
        goals = [f'{goal.id} {goal.title}' for goal in query_set]
        if not goals:
            text = 'Нет целей'
        else:
            text = '\n'.join(goals)
        return self.tg_client.send_message(chat_id=message.chat.id, text=text)

    def _get_categories(self, message: Message, tg_user: TgUser) -> SendMessageResponse:
        """
        Возвращает пользовательские категории или "Нет категорий", если категории не существуют
        :param message: user message
        :param tg_user: telegram user
        :return: Message with user categories
        """
        query_set: QuerySet = GoalCategory.objects.filter(
            board__participants__user=tg_user.user
        ).exclude(is_deleted=True)
        categories: list[str] = [
            f'{category.id} {category.title}' for category in query_set
        ]
        self.states['categories_id'] = [str(cat.id) for cat in query_set]
        if not categories:
            text: str = 'Нет категорий'
        else:
            text = '\n'.join(categories)
        return self.tg_client.send_message(chat_id=message.chat.id, text=text)

    def _create_goal(
        self, chat_id: int, title: str | None, user_id: int, category_id: int | None
    ) -> SendMessageResponse:
        """
        Создание целей
        :param chat_id: user chat id
        :param title: goal title
        :param user_id: user id
        :param category_id: chosen category id
        :return: Message of success creating
        """
        Goal.objects.create(user_id=user_id, title=title, category_id=category_id)
        return self.tg_client.send_message(
            chat_id=chat_id, text=f'Цель {title} создана!'
        )
