# Dowell Chat Backend - V2 Documentation

## Introduction

This documentation provides an overview of the WebSocket events and their usage, as well as information on connecting to the WebSocket.

## Installation

Make sure you have the required dependencies installed:

```bash
pip install -r requirements.txt
```

## Usage
### 1. Start the Django server:
```python
python manage.py runserver
```
### 2. Connect to the WebSocket:
Event triggered when a client connects to the WebSocket. It emits a welcome message to the connected client.
```javascript
const socket = io.connect('https://www.dowellchat.uxlivinglab.online');
```

## WebSocket Events
### `join`
Join a chat room. This event is triggered when a user joins a chat room. It emits a welcome message and previous messages in the room to the user.
```javascript
socket.emit('join', { room: 'your_room_id' });
```
#### Client Listening:
```javascript
socket.on('my_response', (data) => {
    // Handle join response
    console.log(data);
});
```

### `leave`
Leave a chat room. This event is triggered when a user leaves a chat room. It emits a notification to the room.
```javascript
socket.emit('leave', { room: 'your_room_id' });
```
#### Client Listening:
```javascript
socket.on('my_response', (data) => {
    // Handle leave response
    console.log(data);
});
```

### ```message_event```
Send a message to a chat room. This event is used to send messages to a chat room. It includes information about the message type, room ID, message content, sender, and message type.

```javascript
socket.emit('message_event', {
    type: 'text',
    room_id: 'your_room_id',
    message_data: 'Hello, World!',
    side: 'left',
    author: 'John Doe',
    message_type: 'normal',
});
```

#### Client Listening:
```javascript
socket.on('my_response', (data) => {
    // Handle message response
    console.log(data);
});
```
### `callUser`

Initiate an audio/video call. This event is used to initiate an audio/video call, sending signal data and information about the caller to the callee.

```javascript
socket.emit('callUser', {
    signalData: 'your_signal_data',
    from: 'caller_username',
    name: 'caller_name',
    userToCall: 'callee_username',
});
```

#### Client Listening:
```javascript
socket.on('callUser', (data) => {
    // Handle call initiation
    console.log(data);
});
```

### `answerCall`
Answer an audio/video call. This event is used to answer an audio/video call, sending signal data to the caller.
```javascript
socket.emit('answerCall', {
    signal: 'callee_signal_data',
    to: 'caller_username',
});
```
#### Client Listening:
```javascript
socket.on('callAccepted', (data) => {
    // Handle call accepted
    console.log(data);
});
```

### `endCall`
End an ongoing audio/video call. This event is used to signal the end of an ongoing audio/video call.
```javascript
socket.emit('endCall');
```

#### Client Listening:
```javascript
socket.on('callEnded', () => {
    // Handle call ended
});
```
### `disconnect`

Event triggered when a client disconnects from the WebSocket. It emits a 'callEnded' event to signal the end of any ongoing calls.
```javascript
socket.on('disconnect', () => {
    // Handle disconnection
});```