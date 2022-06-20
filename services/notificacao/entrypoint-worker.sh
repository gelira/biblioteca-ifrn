#!/bin/bash

python manage.py migrate

celery -A notificacao worker -l info -n notificacaoworker -Q ${NOTIFICACAO_QUEUE}
