#!/bin/bash

python manage.py migrate
python manage.py one_off_tasks

celery -A avaliacao worker -l info -n avaliacaoworker -Q ${AVALIACAO_QUEUE}
