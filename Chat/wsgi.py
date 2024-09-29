import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Chat.settings')

django.setup()
from websocket.views import sio #noqa
from django.core.wsgi import get_wsgi_application #noqa
import socketio #noqa
from api.utils.datacube_utils import check_connection #noqa
# Get the Django WSGI application

django_app = get_wsgi_application()


socket_connection = check_connection()
if socket_connection:
    print("Connected Safely...")
    application = socketio.WSGIApp(sio, django_app)
    # from gevent import pywsgi
    # from geventwebsocket.handler import WebSocketHandler
    # pywsgi.WSGIServer(('0.0.0.0', 8001), application,
    #                   handler_class=WebSocketHandler).serve_forever()
else:
    print("Connection failed...")
    # application = get_wsgi_application()
    application = django_app

from gevent import pywsgi #noqa
from geventwebsocket.handler import WebSocketHandler #noqa

pywsgi.WSGIServer(('0.0.0.0', 8001), application,
                  handler_class=WebSocketHandler).serve_forever()
