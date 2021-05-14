#!/usr/bin/env bash


./wait-for-postgres.sh db

python manage.py collectstatic --noinput
python manage.py migrate
gunicorn --bind 0.0.0.0:80 config.wsgi

