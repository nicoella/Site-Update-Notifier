import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'site_update_notifier.settings')

app = Celery('site_update_notifier')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()