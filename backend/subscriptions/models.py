from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .constants import (
    VERBOSE_USER, VERBOSE_AUTHOR,
    SUBSCRIPTION_VERBOSE, SUBSCRIPTION_VERBOSE_PLURAL,
    SUB_YOURSELF
)


User = get_user_model()


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name=VERBOSE_USER
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name=VERBOSE_AUTHOR
    )

    class Meta:
        unique_together = ('user', 'author')
        verbose_name = SUBSCRIPTION_VERBOSE
        verbose_name_plural = SUBSCRIPTION_VERBOSE_PLURAL

    def __str__(self):
        return f'{self.user.username} подписан на {self.author.username}'

    def clean(self):
        if self.user == self.author:
            raise ValidationError(SUB_YOURSELF)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
