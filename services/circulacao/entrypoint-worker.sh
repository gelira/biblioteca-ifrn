#!/bin/bash

python manage.py migrate

celery -A circulacao worker -l info -n circulacaoworker -Q ${CIRCULACAO_QUEUE}
