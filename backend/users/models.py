from django.db import models
from django.contrib.auth.models import AbstractUser

from .validators import validate_username
from .constants import (
    VERBOSE_MAIL, VERBOSE_USERNAME, VERBOSE_FIRST, VERBOSE_LAST,
    VERBOSE_PASSWORD, VERBOSE_AVATAR, FOODUSER_VERBOSE,
    FOODUSER_VERBOSE_PLURAL, MAIL_LENGTH, USERNAME_LENGTH, PASSWORD_LENGTH
)


class FoodUser(AbstractUser):
    email = models.EmailField(
        max_length=MAIL_LENGTH,
        unique=True,
        verbose_name=VERBOSE_MAIL)
    username = models.CharField(
        max_length=USERNAME_LENGTH,
        unique=True,
        verbose_name=VERBOSE_USERNAME,
        validators=(validate_username,))
    first_name = models.CharField(
        max_length=USERNAME_LENGTH,
        verbose_name=VERBOSE_FIRST)
    last_name = models.CharField(
        max_length=USERNAME_LENGTH,
        verbose_name=VERBOSE_LAST)
    password = models.CharField(
        max_length=PASSWORD_LENGTH,
        verbose_name=VERBOSE_PASSWORD)
    avatar = models.ImageField(
        upload_to='users/images/',
        null=True,
        blank=True,
        default=None,
        verbose_name=VERBOSE_AVATAR
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name', 'password')

    class Meta:
        verbose_name = FOODUSER_VERBOSE
        verbose_name_plural = FOODUSER_VERBOSE_PLURAL

    def __str__(self):
        return self.username
