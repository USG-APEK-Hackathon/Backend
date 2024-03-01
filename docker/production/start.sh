#!/bin/bash

python manage.py migrate

exec gunicorn --bind 0.0.0.0:8000 --workers 4 config.wsgi:application
