#!/bin/bash

python manage.py migrate

celery -A avaliacao worker -l info -n avaliacaoworker -Q ${AVALIACAO_QUEUE}
