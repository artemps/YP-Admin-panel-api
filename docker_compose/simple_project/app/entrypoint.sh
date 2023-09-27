#!/bin/sh

echo "Waiting for postgres... $POSTGRES_HOST $POSTGRES_PORT"

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.5
done

echo "PostgreSQL started"

python3 manage.py collectstatic --no-input
python3 manage.py migrate

uwsgi --ini uwsgi.ini