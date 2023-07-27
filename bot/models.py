from django.db import models
from django.utils.crypto import get_random_string

from core.models import User


class TgUser(models.Model):
    """
    Модель пользователя Telegram
    """

    chat_id = models.BigIntegerField(unique=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, default=None
    )
    verification_code = models.CharField(
        max_length=50, null=True, blank=True, default=None
    )

    @property
    def is_verified(self) -> bool:
        return bool(self.user)

    @staticmethod
    def generate_verification_code() -> str:
        """
        Сгенерировать проверочный код
        :return: verification code
        """
        return get_random_string(length=50)

    def update_verification_code(self) -> None:
        self.verification_code = self.generate_verification_code()
        self.save(update_fields=['verification_code'])

    class Meta:
        verbose_name = 'Телеграмм-пользователь'
        verbose_name_plural = 'Телеграмм-пользователи'

    def __str__(self):
        return self.chat_id
