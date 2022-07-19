"""
WSGI config for avaliacao project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import dotenv
from pathlib import Path
from django.core.wsgi import get_wsgi_application

env_path = Path(__file__).parent.parent / '.env'

if env_path.is_file():
    dotenv.read_dotenv(env_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catalogo.settings')

application = get_wsgi_application()
