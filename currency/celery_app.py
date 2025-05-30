import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'currency.settings')

app = Celery('currency')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

from .celery_schedule import CELERYBEAT_SCHEDULE
app.conf.beat_schedule = CELERYBEAT_SCHEDULE