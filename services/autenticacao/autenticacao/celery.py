from __future__ import absolute_import, unicode_literals

import os
import dotenv
import django

dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autenticacao.settings')

django.setup()

from celery import Celery
from celery.signals import after_task_publish
from django_celery_beat.models import PeriodicTask

app = Celery('autenticacao')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@after_task_publish.connect
def signal(headers=None, **kwargs):
    if not headers:
        return

    try:
        periodic_task_name = headers.get('periodic_task_name')
    except:
        periodic_task_name = None

    if periodic_task_name:
        PeriodicTask.objects.filter(name=periodic_task_name).update(enabled=False)
