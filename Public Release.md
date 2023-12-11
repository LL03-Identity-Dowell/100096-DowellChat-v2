# Living Lab Chat Public Documentation

## Overview

This documentation serves as a comprehensive guide to the Living Lab Chat server events, their applications, and details on connecting to the server.

Note: To begin, ensure that you have obtained an API key from:
[DoWell API Key System](https://1105-ai-dowell.github.io/100105-DoWellApiKeySystem/)


## Connecting to the Server

### 1. Establishing Connection
When a client connects to the server, an event is triggered, and a welcome message is emitted to the connected client.
```javascript
var livinglab = io('https://www.dowellchat.uxlivinglab.online/', { query: `api_key=${'your-api-key'}` });
```
### 2. Handling Connection Errors
In case of a connection error, this event will be triggered, allowing you to handle the error appropriately, such as displaying an alert or logging it.

```javascript
livinglab.on('connect_error', function(error) {
// Handle the connection error
console.error(error.message);
});
```

## Living Lab Chat Events
### `join`
Initiating a chat room connection. This event is triggered when a user joins a chat room, emitting a welcome message and previous messages to the user.
```javascript
livinglab.emit('join', { room: 'your_room_id' });
```
#### Client Listening:
```javascript
livinglab.on('my_response', (data) => {
    // Handle join response
    console.log(data);
});
```

### `leave`
Exiting a chat room. This event is triggered when a user leaves a chat room, emitting a notification to the room.

```javascript
livinglab.emit('leave', { room: 'your_room_id' });
```
#### Client Listening:
```javascript
livinglab.on('my_response', (data) => {
    // Handle leave response
    console.log(data);
});
```

### ```message_event```
Sending a message to a chat room. This event facilitates sending messages, providing details about the message type, room ID, content, sender, and message type.

```javascript
livinglab.emit('message_event', {
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
livinglab.on('my_response', (data) => {
    // Handle message response
    console.log(data);
});
```
### `callUser`

Initiating an audio/video call. This event is used to start an audio/video call, sending signal data and caller information to the callee.

```javascript
livinglab.emit('callUser', {
    signalData: 'your_signal_data',
    from: 'caller_username',
    name: 'caller_name',
    userToCall: 'callee_username',
});
```

#### Client Listening:
```javascript
livinglab.on('callUser', (data) => {
    // Handle call initiation
    console.log(data);
});
```

### `answerCall`
Responding to an audio/video call. This event is used to answer a call, sending signal data to the caller.
```javascript
livinglab.emit('answerCall', {
    signal: 'callee_signal_data',
    to: 'caller_username',
});
```
#### Client Listening:
```javascript
livinglab.on('callAccepted', (data) => {
    // Handle call accepted
    console.log(data);
});
```

### `endCall`
Terminating an ongoing audio/video call. This event signals the end of an ongoing call.
```javascript
livinglab.emit('endCall');
```

#### Client Listening:
```javascript
livinglab.on('callEnded', () => {
    // Handle call ended
});
```
### `disconnect`

When a client disconnects from the server, this event is triggered, emitting a 'callEnded' event to signify the end of any ongoing calls.
```javascript
livinglab.on('disconnect', () => {
    // Handle disconnection
});```