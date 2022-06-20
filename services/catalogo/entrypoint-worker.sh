#!/bin/bash

python manage.py migrate
python manage.py one_off_tasks

celery -A catalogo worker -l info -n catalogoworker -Q ${CATALOGO_QUEUE}
