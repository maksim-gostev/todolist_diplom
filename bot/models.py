from django.db import models
from django.utils.crypto import get_random_string
from core.models import User


class TgUser(models.Model):
    chat_id = models.PositiveBigIntegerField(primary_key=True, editable=False, unique=True)
    username = models.CharField(max_length=250, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    verification_code = models.CharField(max_length=50, null=True, blank=True, unique=True)

    class Meta:
        verbose_name = 'Телеграмм-пользователь'
        verbose_name_plural = 'Телеграмм-пользователи'

    @property
    def is_verified(self) -> bool:
        return bool(self.user)

    def __str__(self):
        return f'{self.__class__.__name__}({self.chat_id})'

    @staticmethod
    def _generate_verification_cod() -> str:
        return get_random_string(20)

    def update_verification_cod(self) -> None:
        self.verification_code = self._generate_verification_cod()
        self.save(update_fields=['verification_code'])
