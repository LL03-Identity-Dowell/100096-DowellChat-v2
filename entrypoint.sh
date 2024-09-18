#!/bin/sh



# Apply database migrations
python manage.py migrate --noinput

# Create superuser if it doesn't already exist
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'pass123456')
END

# Start the application using Gunicorn with WebSocket support
gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 Chat.wsgi:application --timeout 9999
