"""
ASGI config for autenticacao project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
import dotenv
from pathlib import Path
from django.core.asgi import get_asgi_application

env_path = Path(__file__).parent.parent / '.env'

if env_path.is_file():
    dotenv.read_dotenv(env_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autenticacao.settings')

application = get_asgi_application()
