from __future__ import absolute_import, unicode_literals

import os
import dotenv
from celery import Celery

dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notificacao.settings')

app = Celery('aquisicao')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
