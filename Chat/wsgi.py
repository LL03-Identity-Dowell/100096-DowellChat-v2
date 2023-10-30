import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Chat.settings')
import socketio


from django.core.wsgi import get_wsgi_application

django_app= get_wsgi_application()
from api.views import sio
application = socketio.WSGIApp(sio, django_app)
