import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wade.settings')

app = Celery('wade')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()