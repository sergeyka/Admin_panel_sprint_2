#!/usr/bin/env bash

python manage.py collectstatic --noinput
python manage.py migrate
gunicorn --bind 0.0.0.0:80 config.wsgi

