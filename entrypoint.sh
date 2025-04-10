#!/bin/bash

# Démarrer PostgreSQL
service postgresql start

# Créer DB et user si pas déjà fait
su - postgres -c "psql -tc \"SELECT 1 FROM pg_user WHERE usename = 'instagenda';\" | grep -q 1 || psql -c \"CREATE USER instagenda WITH PASSWORD 'dev';\"" &&
su - postgres -c "psql -lqt | cut -d \| -f 1 | grep -qw instagenda || createdb -O instagenda instagenda"

# Démarrer Redis
redis-server --daemonize yes

# Appliquer les migrations
cd /app/api
pipenv run python manage.py migrate

# Lancer celery en arrière-plan
pipenv run celery -A api worker --loglevel=info &

# Lancer Django en arrière-plan sur port 8000
pipenv run python manage.py runserver 127.0.0.1:8000 &

# Lancer nginx
nginx -g 'daemon off;'