async_mode = None

from .models import Room, Message
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

from .serializers import MessageSerializer

#Socket imports
import os
from django.http import HttpResponse
import socketio

# # basedir = os.path.dirname(os.path.realpath(__file__))
sio = socketio.Server(cors_allowed_origins="*", async_mode=async_mode)
app = socketio.WSGIApp(sio)
thread = None

@api_view(['GET'])
@csrf_exempt
def index(request):
    global thread
    if thread is None:
        thread = sio.start_background_task(background_thread)
    return HttpResponse("This URL is for WebSocket connections")
    # return HttpResponse(open(os.path.join(basedir, 'static/index.html')))
    # if request.method == 'GET':
    #     return HttpResponse("This URL is for WebSocket connections")
    # else:
    #     return app.handle_request(request)

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

def close_room(sid, message):
    sio.emit('my_response',
             {'data': 'Room ' + message['room'] + ' is closing.'},
             room=message['room'])
    sio.close_room(message['room'])

# @sio.event
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


# message=["Hello Everyone", "This is the second message"]


@sio.event
def connect(sid, environ, query_para):
    sio.emit('my_response', {'data': "Welcome to Dowell Chat", 'count': 0}, room=sid)
    sio.emit('me', sid)


@sio.event
def disconnect(sid):
    sio.emit('callEnded',  skip_sid=sid)
    print('Client disconnected')


""" WEB RTC SIGNALING SERVER SECTION"""


# peer_connections = {}
#
#
# @sio.event
# def disconnect(sid):
#     # Cleanup and remove the peer connection data
#     if sid in peer_connections:
#         recipient_sid = peer_connections[sid]["recipient_sid"]
#         if recipient_sid in peer_connections:
#             # Notify the recipient about the disconnect
#             sio.emit('peer_disconnected', room=recipient_sid, namespace='/webrtc')
#             del peer_connections[recipient_sid]
#         del peer_connections[sid]
#     print(f"Client {sid} disconnected from /webrtc namespace")
#
#
# # Handle offer messages
# # @sio.event(namespace='/webrtc')
# @sio.event
# def offer(sid, message):
#     recipient_sid = message['recipient_sid']
#     offer = message['offer']
#
#     # Store the offer in the peer_connections dictionary
#     peer_connections[sid] = {"recipient_sid": recipient_sid, "offer": offer}
#
#     # Forward the offer to the recipient
#     # sio.emit('offer', {'offer': offer, 'sender_sid': sid}, room=recipient_sid, namespace='/webrtc')
#     sio.emit('offer', {'offer': offer, 'sender_sid': sid}, room=recipient_sid)
#
# # Handle answer messages
# # @sio.event(namespace='/webrtc')
# @sio.event
# def answer(sid, message):
#     sender_sid = message['sender_sid']
#     answer = message['answer']
#
#     # Forward the answer to the sender
#     # sio.emit('receive_answer', {'answer': answer, 'sender_sid': sid}, room=sender_sid, namespace='/webrtc')
#     sio.emit('receive_answer', {'answer': answer, 'sender_sid': sid}, room=sender_sid)
#
# # @sio.event(namespace='/webrtc')
# @sio.event
# def ice_candidate(sid, message):
#     recipient_sid = message['recipient_sid']
#     ice_candidate = message['ice_candidate']
#
#     # Forward the ICE candidate to the recipient
#     # sio.emit('receive_ice_candidate', {'ice_candidate': ice_candidate, 'sender_sid': sid}, room=recipient_sid, namespace='/webrtc')
#     sio.emit('receive_ice_candidate', {'ice_candidate': ice_candidate, 'sender_sid': sid}, room=recipient_sid)
#
#
#
# # Audio call signaling
# @sio.event
# def audio_offer(sid, message):
#     recipient_sid = message['recipient_socket_id']  # Recipient's socket.id
#     offer = message['offer']
#
#     # Store the audio call offer in the peer_connections dictionary
#     peer_connections[sid] = {"recipient_sid": recipient_sid, "audio_offer": offer}
#
#     # Forward the audio call offer to the recipient
#     sio.emit('audio_offer', {'offer': offer, 'sender_sid': sid}, room=recipient_sid)
#
#
# @sio.event
# def audio_answer(sid, message):
#     sender_sid = message['sender_sid']
#     answer = message['answer']
#
#     # Forward the audio call answer to the sender
#     sio.emit('audio_answer', {'answer': answer, 'sender_sid': sid}, room=sender_sid)
#
# @sio.event
# def audio_ice_candidate(sid, message):
#     recipient_sid = message['recipient_sid']
#     ice_candidate = message['ice_candidate']
#
#     # Forward the audio call ICE candidate to the recipient
#     sio.emit('audio_ice_candidate', {'ice_candidate': ice_candidate, 'sender_sid': sid}, room=recipient_sid)
#


"""New Video Call Feature"""
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
