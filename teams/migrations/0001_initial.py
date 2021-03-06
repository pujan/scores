# Generated by Django 3.1.4 on 2021-01-07 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='nazwa')),
                ('flag', models.ImageField(upload_to='static/images/flags', verbose_name='flaga')),
            ],
            options={
                'verbose_name': 'kraj',
                'verbose_name_plural': 'kraje',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Kind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='nazwa')),
            ],
            options={
                'verbose_name': 'rodzaj',
                'verbose_name_plural': 'rodzaje',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='nazwa')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='static/images/teams', verbose_name='logo/flaga')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='teams.country', verbose_name='kraj')),
                ('kind', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='teams.kind', verbose_name='rodzaj')),
            ],
            options={
                'verbose_name': 'drużyna',
                'verbose_name_plural': 'drużyny',
                'ordering': ('kind', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(verbose_name='rozpoczęcie')),
                ('score_team_home', models.IntegerField(blank=True, help_text='grającej u siebie', null=True, verbose_name='Punkty dużyny')),
                ('score_team_away', models.IntegerField(blank=True, help_text='grającej na wyjeździe', null=True, verbose_name='Punkty drużyny')),
                ('finished', models.BooleanField(default=False, verbose_name='zakończony')),
                ('continues', models.BooleanField(default=False, verbose_name='w trakcie')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='czas aktualizacji')),
                ('team_away', models.ForeignKey(help_text='grająca na wyjeździe', on_delete=django.db.models.deletion.CASCADE, related_name='matches_away', to='teams.team', verbose_name='Drużyna')),
                ('team_home', models.ForeignKey(help_text='grająca u siebie', on_delete=django.db.models.deletion.CASCADE, related_name='matches_home', to='teams.team', verbose_name='Drużyna')),
            ],
            options={
                'verbose_name': 'mecz',
                'verbose_name_plural': 'mecze',
                'ordering': ('-time',),
            },
        ),
    ]
