
from django.db import models
from django.contrib.auth.models import User


class Subscription(models.Model):
    
    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'model'],
                name='unique_user_model')]

        indexes = [
            models.Index(fields=['user'], name='subscription_user_idx'),
            models.Index(fields=['user', 'model'], name='subscription_user_model_idx')]

        ordering = ['user']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        blank = False,
        verbose_name = 'Пользователь')
    
    model = models.CharField(
        max_length = 50,
        blank = False,
        verbose_name = 'Имя модели объекта')

    @property
    def repr(self) -> str:
        if self.id:
            return f'{self.user} ({self.model})'[:255]
        else:
            return 'Подписка (новая)'

    def __str__(self):
        return self.repr

    def __repr__(self):
        return self.repr
