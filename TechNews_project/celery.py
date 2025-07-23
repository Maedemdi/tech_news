import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TechNews_project.settings')

app = Celery('TechNews_project')
app.config_from_object('django.conf:settings', namespace= 'CELERY')
app.autodiscover_tasks()