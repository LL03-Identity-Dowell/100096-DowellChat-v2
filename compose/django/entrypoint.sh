#!/bin/sh

# Wait for PostgreSQL to be available
while ! nc -z postgres 5432; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done

# Run migrations
python manage.py migrate

# Start the Django application with gunicorn
exec gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 Chat.wsgi:application --timeout 9999
