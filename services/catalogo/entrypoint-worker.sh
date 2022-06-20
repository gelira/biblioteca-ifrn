#!/bin/bash

python manage.py migrate

celery -A catalogo worker -l info -n catalogoworker -Q ${CATALOGO_QUEUE}
