import time
async_mode = 'gevent'
# async_mode = "threading"
from .models import Room, Message
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
<<<<<<< HEAD
from django.views import View

=======
>>>>>>> 13614be5b6f27a65e9ab62c5b5ccb119ad003653
from .serializers import MessageSerializer
from .utils import processApiService, DataCubeConnection
#Socket imports
import os
from django.http import HttpResponse
import socketio
sio = socketio.Server(cors_allowed_origins="*", async_mode=async_mode)
app = socketio.WSGIApp(sio)
thread = None

@api_view(['GET'])
@csrf_exempt
def index(request):
    global thread
    if thread is None:
        thread = sio.start_background_task(background_thread)
    return HttpResponse("Connected to Dowell Chat Backend")


def background_thread():
    count = 0
    while True:
        sio.sleep(10)
        count += 1
        sio.emit('my_response', {'data': 'Server generated event'},
                 namespace='/test')

@sio.event
def join(sid, message):
    room = message['room']
    sio.enter_room(sid, room)
    messages = Message.objects.filter(room_id=message['room']).all()
    sio.emit('my_response', {'data': f"{sid} Joined the Room",  'count': 0}, room=room, skip_sid=sid)
    if messages.count()==0:
        sio.emit('my_response', {'data': "Hey how may i help you",  'count': 0}, room=sid)
    else:
        for i in messages:
            sio.emit('my_response', {'data': str(i.message_data),  'count': 0}, room=sid)

@sio.event
def leave(sid, message):
    sio.leave_room(sid, message['room'])
    sio.emit('my_response', {'data': 'Left room: ' + message['room']},
             room=message['room'])
    
@sio.event
def close_room(sid, message):
    sio.emit('my_response',
             {'data': 'Room ' + message['room'] + ' is closing.'},
             room=message['room'])
    sio.close_room(message['room'])

@sio.event
def message_event(sid, message):
    type = message['type']
    room_id = message['room_id']
    message_data = message['message_data']
    side = message['side']
    author = message['author']
    message_type = message['message_type']

    data = {
        "type": type,
        "room_id": room_id,
        "message_data": message_data,
        "side": side,
        "author": author,
        "message_type": message_type,
    }
    serializer = MessageSerializer(data=data)
    if serializer.is_valid():

        Message.objects.create(
            type = type,
            room_id = room_id,
            message_data = message_data,
            side = side,
            author = author,
            message_type = message_type
        )
        return sio.emit('my_response', {'data': message['message_data'], 'sid':sid},  room=message['room_id'])
    else:
        return sio.emit('my_response', {'data': 'Invalid Data', 'sid':sid}, room=message['room'])


# #   skip_sid=sid,
@sio.event
def disconnect_request(sid):
    sio.disconnect(sid)


@sio.event
def connect(sid, environ, query_para):
    sio.emit('my_response', {'data': "Welcome to Dowell Chat", 'count': 0}, room=sid)
    sio.emit('me', sid, room=sid)


@sio.event
def disconnect(sid):
    sio.emit('callEnded',  skip_sid=sid)
    print('Client disconnected')


""" WEB RTC SIGNALING SERVER SECTION"""
@sio.event
def callUser(sid, data):
    sio.emit('callUser', {
        'signal': data['signalData'],
        'from': data['from'],
        'name': data['name']
    }, room=data['userToCall'])

@sio.event
def answerCall(sid, data):
    sio.emit('callAccepted', data['signal'], room=data['to'])

<<<<<<< HEAD

class SSLVerificationView(View):
    def get(self, request, *args, **kwargs):
        txt_content = "D873E6BC2B961D3D6CD212A292FE485BCDF8D3EFBF45E4A8A84B0B84ACEF3A8E\ncomodoca.com\n69b1fa11cd1fdaa"
        return HttpResponse(txt_content, content_type="text/plain")
=======
@sio.event
def endCall(sid):
    sio.emit('callEnded')



"""PUBLIC RELEASE"""
public_namespace = '/public'
@api_view(['GET'])
@csrf_exempt
def public(request):
    return HttpResponse("Connected to Public Dowell Chat Backend")

class PublicNamespace(socketio.Namespace):

    def on_connect(self, sid, environ):
        query_params = environ.get("QUERY_STRING")
        query_dict = dict(qc.split("=") for qc in query_params.split("&"))

        if 'api_key' in query_dict:
            api_key = query_dict['api_key']
            authentication_res = processApiService(str(api_key))

            if authentication_res['success'] == False:
                error_message= f'User {sid} connection denied due to api key {authentication_res["message"]}' 
                print(authentication_res)
                raise socketio.exceptions.ConnectionRefusedError(error_message)
            else:
                print(f'User {sid} connected with valid input data: {api_key}')
                sio.emit('my_response', {'data': "Welcome to Public Dowell Chat", 'count': 0}, room=sid, namespace='/public')
                sio.emit('me', sid, room=sid, namespace='/public')
                
        else:
            error_message= f'User {sid} connection denied due to no Api Key was provided'        
            raise socketio.exceptions.ConnectionRefusedError(error_message)
    
        

    def on_disconnect(self, sid):
        pass

    def on_join(sid, message):
        room = message['room']


        sio.enter_room(sid, room)
        messages = Message.objects.filter(room_id=message['room']).all()

        sio.emit('my_response', {'data': f"{sid} Joined the Room",  'count': 0}, room=room, skip_sid=sid)

        if messages.count()==0:
            sio.emit('my_response', {'data': "Hey how may i help you",  'count': 0}, room=sid)
        else:
            for i in messages:
                sio.emit('my_response', {'data': str(i.message_data),  'count': 0}, room=sid)

    def on_leave(sid, message):
        sio.leave_room(sid, message['room'])
        sio.emit('my_response', {'data': 'Left room: ' + message['room']},
                room=message['room'])

    def on_close_room(sid, message):
        sio.emit('my_response',
                {'data': 'Room ' + message['room'] + ' is closing.'},
                room=message['room'])
        sio.close_room(message['room'])

    
    def on_message_event(sid, message):
        type = message['type']
        room_id = message['room_id']
        message_data = message['message_data']
        side = message['side']
        author = message['author']
        message_type = message['message_type']

        data = {
            "type": type,
            "room_id": room_id,
            "message_data": message_data,
            "side": side,
            "author": author,
            "message_type": message_type,
        }
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():

            Message.objects.create(
                type = type,
                room_id = room_id,
                message_data = message_data,
                side = side,
                author = author,
                message_type = message_type
            )
            return sio.emit('my_response', {'data': message['message_data'], 'sid':sid},  room=message['room_id'])
        else:
            return sio.emit('my_response', {'data': 'Invalid Data', 'sid':sid}, room=message['room'])

    def on_callUser(sid, data):
        sio.emit('callUser', {
            'signal': data['signalData'],
            'from': data['from'],
            'name': data['name']
        }, room=data['userToCall'])

    def on_answerCall(sid, data):
        sio.emit('callAccepted', data['signal'], room=data['to'])

    def on_endCall(sid):
        sio.emit('callEnded')

sio.register_namespace(PublicNamespace('/public'))
>>>>>>> 13614be5b6f27a65e9ab62c5b5ccb119ad003653
