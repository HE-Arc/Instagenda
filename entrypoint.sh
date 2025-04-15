#!/bin/bash

# Start postgresql
service postgresql start

# Create the database
su - postgres -c "psql -tc \"SELECT 1 FROM pg_user WHERE usename = 'instagenda';\" | grep -q 1 || psql -c \"CREATE USER instagenda WITH PASSWORD 'dev';\"" &&
su - postgres -c "psql -lqt | cut -d \| -f 1 | grep -qw instagenda || createdb -O instagenda instagenda"

# Start Redis
redis-server --daemonize yes

# Apply the migrations
cd /app/api
pipenv run python manage.py migrate

python manage.py collectstatic

# Launch celery in the background
pipenv run celery -A instagenda worker --loglevel=info &

pipenv run gunicorn instagenda.wsgi:application --bind 0.0.0.0:9000 --workers 3 --timeout 120 &

# Launch nginx
nginx -g 'daemon off;'