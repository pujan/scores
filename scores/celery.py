import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scores.settings')
app = Celery('scores')

# można zdefiniować w adminie: Crontabs i Periodic tasks
app.conf.beat_schedule = {
    'send_email-every-monday': {
        'task': 'teams.tasks.send_email',
        'schedule': crontab(hour=7, minute=30, day_of_week=1),
        'args': ('week',),
    },
    'send_email-every-day': {
        'task': 'teams.tasks.send_email',
        'schedule': crontab(hour=7, minute=30),
        'args': ('day',),
    },
    'endpoint-every-monday': {
        'task': 'teams.tasks.post_to_endpoint',
        'schedule': crontab(hour=7, minute=30, day_of_week=1),
        'args': ('week',),
    },
    'endpoint-every-day': {
        'task': 'teams.tasks.post_to_endpoint',
        'schedule': crontab(hour=7, minute=30),
        'args': ('day',),
    },
    'send_email-live': {
        'task': 'teams.tasks.send_email',
        'schedule': crontab(minute='*/5'),
        'args': ('live',),
    },
    'endpoint-live': {
        'task': 'teams.tasks.post_to_endpoint',
        'schedule': crontab(minute='*/5'),
        'args': ('live',),
    },
    'update-score-realtime': {
        'task': 'teams.tasks.update_scores',
        'schedule': crontab(minute='*/1'),
    }
}

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
