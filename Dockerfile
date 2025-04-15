FROM python:3.11.9-slim

# Install all dependencies
RUN apt-get update && apt-get install -y \
    curl build-essential git libpq-dev wget gnupg \
    redis-server postgresql postgresql-contrib \
    nginx \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && pip install pipenv \
    && apt-get clean

# Create the app directory
WORKDIR /app

# Copy all the files of the project
COPY . .

# Install backend (Django)
WORKDIR /app/api
RUN pipenv install --deploy --ignore-pipfile

RUN pipenv install gunicorn

# Build frontend
WORKDIR /app/frontend
RUN npm install && npm run build

# Copy the frontend build to the nginx folder
RUN mkdir -p /var/www/frontend
RUN cp -r dist/* /var/www/frontend/

# Copy the nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose the ports
EXPOSE 80 8000

# Entrypoint
ENTRYPOINT ["/entrypoint.sh"]
