FROM python:3.11-slim

# Installer dépendances système
RUN apt-get update && apt-get install -y \
    curl build-essential git libpq-dev wget gnupg \
    redis-server postgresql postgresql-contrib \
    nginx \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && pip install pipenv \
    && apt-get clean

# Créer dossier app
WORKDIR /app

# Copier tous les fichiers du projet
COPY . .

# Installer backend (Django)
WORKDIR /app/api
RUN pipenv install --deploy --ignore-pipfile

RUN pipenv install gunicorn

# Builder frontend
WORKDIR /app/frontend
RUN npm install && npm run build

# Copier le build frontend dans un dossier nginx
RUN mkdir -p /var/www/frontend
RUN cp -r dist/* /var/www/frontend/

# Copier config Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Copier script de démarrage
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Exposer les ports
EXPOSE 80 8000

# Entrypoint
ENTRYPOINT ["/entrypoint.sh"]
