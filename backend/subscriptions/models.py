from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscriptions'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscribers'
    )

    class Meta:
        unique_together = ('user', 'author')

    def __str__(self):
        return f'{self.user.username} subscribed to {self.author.username}'
