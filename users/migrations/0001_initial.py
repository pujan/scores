# Generated by Django 3.1.4 on 2021-01-07 14:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.TextField(choices=[('week', 'Co tydzień'), ('day', 'W dzień meczu'), ('live', 'Na żywo')], verbose_name='typ')),
                ('method', models.TextField(choices=[('endpoint', 'API'), ('email', 'Wyślij e-mail')], verbose_name='rodzaj powiadomiwnia')),
                ('url', models.URLField(blank=True, null=True, verbose_name='URL')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='e-mail')),
                ('teams', models.ManyToManyField(related_name='subscribes', to='teams.Team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribe', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
