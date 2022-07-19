#!/bin/bash

python manage.py migrate
python manage.py one_off_tasks

celery -A autenticacao beat -l info
