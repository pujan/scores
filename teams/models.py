import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Kind(models.Model):
    name = models.CharField(max_length=20, verbose_name='nazwa')

    class Meta:
        verbose_name = 'rodzaj'
        verbose_name_plural = 'rodzaje'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=50, verbose_name='nazwa')
    flag = models.ImageField(upload_to='static/images/flags', verbose_name='flaga')

    class Meta:
        verbose_name = 'kraj'
        verbose_name_plural = 'kraje'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name='nazwa')
    logo = models.ImageField(null=True, blank=True, upload_to='static/images/teams', verbose_name='logo/flaga')
    country = models.ForeignKey(Country, null=True, blank=True, related_name='teams', on_delete=models.CASCADE,
                                verbose_name='kraj')
    kind = models.ForeignKey(Kind, related_name='teams', on_delete=models.CASCADE, verbose_name='rodzaj')

    class Meta:
        verbose_name = 'drużyna'
        verbose_name_plural = 'drużyny'
        ordering = ('kind', 'name')

    def __str__(self):
        return self.name


class Match(models.Model):
    time = models.DateTimeField(verbose_name='rozpoczęcie')
    team_home = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_home', verbose_name='Drużyna',
                                  help_text='grająca u siebie')
    team_away = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_away', verbose_name='Drużyna',
                                  help_text='grająca na wyjeździe')
    score_team_home = models.IntegerField(verbose_name='Punkty dużyny', null=True, blank=True,
                                          help_text='grającej u siebie')
    score_team_away = models.IntegerField(verbose_name='Punkty drużyny', null=True, blank=True,
                                          help_text='grającej na wyjeździe')
    finished = models.BooleanField(verbose_name='zakończony', default=False)
    continues = models.BooleanField(verbose_name='w trakcie', default=False)
    updated_at = models.DateTimeField(verbose_name='czas aktualizacji', auto_now=True, blank=True)

    class Meta:
        verbose_name = 'mecz'
        verbose_name_plural = 'mecze'
        ordering = ('-time',)

    def archive(self):
        time_archive = timezone.now() - datetime.timedelta(days=14)
        return self.finished and self.time < time_archive
    archive.admin_order_field = 'time'
    archive.boolean = True
    archive.short_description = 'Czy archiwalny'

    def clean(self):
        if self.team_home.pk == self.team_away.pk:
            raise ValidationError('Drużyna nie może grać sama ze sobą')

    def __str__(self):
        return f'{self.team_home} - {self.team_away}'
