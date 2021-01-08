from django.conf import settings
from django.db import models
from teams.models import Team

User = settings.AUTH_USER_MODEL


class Subscriber(models.Model):
    TYPES = (
        ('week', 'Co tydzień'),
        ('day', 'W dzień meczu'),
        ('live', 'Na żywo'),
    )
    METHODS = (
        ('endpoint', 'API'),
        ('email', 'Wyślij e-mail'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribe')
    type = models.TextField(choices=TYPES, verbose_name='typ')
    method = models.TextField(choices=METHODS, verbose_name='rodzaj powiadomiwnia')
    teams = models.ManyToManyField(Team, related_name='subscribes')
    url = models.URLField(null=True, blank=True, verbose_name='URL')
    email = models.EmailField(null=True, blank=True, verbose_name='e-mail')

    def __str__(self):
        return self.user.username
