#!/bin/sh

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
rm db.sqlite3

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --username admin --email example@example.com