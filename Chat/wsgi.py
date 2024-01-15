# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Chat.settings')
# import socketio
# from django.core.wsgi import get_wsgi_application
#
# django_app= get_wsgi_application()
# from api.views import sio
#
# # application = socketio.WSGIApp(sio, django_app)
# # Using eventlet to run the server
# import eventlet
# application = socketio.WSGIApp(sio, django_app)
#
# # Binding to the port
# eventlet.wsgi.server(eventlet.listen(('', 8000)), application)

# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Chat.settings')
# import socketio
# from django.core.wsgi import get_wsgi_application
#
# # Get the Django WSGI application
# django_app = get_wsgi_application()
#
# # Setup socketio server
# sio = socketio.Server(cors_allowed_origins="*")
# application = socketio.WSGIApp(sio, django_app)
#
# if __name__ == "__main__":
#     import eventlet
#
#     # Start the server using eventlet
#     eventlet.wsgi.server(eventlet.listen(('', 8000)), application)

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Chat.settings')
import socketio

from django.core.wsgi import get_wsgi_application

# Get the Django WSGI application
django_app = get_wsgi_application()

from api.views import sio

application = socketio.WSGIApp(sio, django_app)
# from gevent import pywsgi
# from geventwebsocket.handler import WebSocketHandler
# pywsgi.WSGIServer(('', 8001), application,
#                   handler_class=WebSocketHandler).serve_forever()
