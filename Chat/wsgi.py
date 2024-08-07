import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Chat.settings')
import socketio

from django.core.wsgi import get_wsgi_application

# Get the Django WSGI application
django_app = get_wsgi_application()

from websocket.views import sio
from api.utils.datacube_utils import check_connection

socket_connection = check_connection()
if socket_connection:
    application = socketio.WSGIApp(sio, django_app)
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    pywsgi.WSGIServer(('0.0.0.0', 8001), application,
                    handler_class=WebSocketHandler).serve_forever()
else:
    application = get_wsgi_application()
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    pywsgi.WSGIServer(('0.0.0.0', 8001), application,
                    handler_class=WebSocketHandler).serve_forever()