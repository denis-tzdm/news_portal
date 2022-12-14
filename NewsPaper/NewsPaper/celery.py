import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'send_digest_weekly': {
        'task': 'notifier.tasks.send_digest',
        'schedule': crontab(day_of_week="monday",
                            hour="12",
                            minute="00"),
    },
}

app.autodiscover_tasks()
