from __future__ import absolute_import, unicode_literals

import os
import dotenv
from celery import Celery
from pathlib import Path

env_path = Path(__file__).parent.parent / '.env'

if env_path.is_file():
    dotenv.read_dotenv(env_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autenticacao.settings')

app = Celery('gateway')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
