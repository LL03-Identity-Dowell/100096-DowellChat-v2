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
});
```


## Customer Support Ticket System Section

### ```Create Topic```
This event is used to create a new topic 

```javascript
socket.emit('create_topic', {
    name: "Name of Topic",
    workspace_id: "Your workspace ID",
    api_key: "Your ApI Key",
    created_at: "Date of Creation"
});
```

#### Client Listening:
```javascript
socket.on('setting_response', (data) => {
    // Handle response for the event
    console.log(data);
});
```

### ```Get  All Topics```
This event returns all the topics in a particular workspace

```javascript
socket.emit('get_all_topics', {
    workspace_id: "Your workspace ID",
    api_key: "Your ApI Key",
});
```

#### Client Listening:
```javascript
socket.on('setting_response', (data) => {
    // Handle response for the event
    console.log(data);
});
```

### ```Create Line Manager```
This event creates a new line manager

```javascript
socket.emit('create_line_manager', {
    user_id: "UserID of the line manager",
    positions_in_a_line: "Position in line",
    average_serving_time: "Average Servering time",
    ticket_count: 0,
    workspace_id: "Your workspace ID",
    api_key: "Your ApI Key",
    created_at: "Date of creation"
});
```

#### Client Listening:
```javascript
socket.on('setting_response', (data) => {
    // Handle response for the event
    console.log(data);
});
```

### ```Get  All Line Managers```
This event returns all the line managers in a particular workspace

```javascript
socket.emit('get_all_line_managers', {
    workspace_id: "Your workspace ID",
    api_key: "Your ApI Key",
});
```

#### Client Listening:
```javascript
socket.on('setting_response', (data) => {
    // Handle response for the event
    console.log(data);
});
```

### ```Ticket message event```
Send a message to a chat room. This event is used to send messages to a chat room. 

```javascript
socket.emit('ticket_message_event', {
    ticket_id: "ID of the ticket the message is coming from",
    product: "The Product name",
    message_data: "Content of the message",
    user_id: "UserID of the sender",
    reply_to: "None",
    workspace_id: "Your workspace ID",
    api_key: "Your ApI Key",
    created_at: "Date of Creation"
});
```

#### Client Listening:
```javascript
socket.on('ticket_message_response', (data) => {
    // Handle response for the event
    console.log(data);
});
```
### ```Get  Ticket Messages```
This event returns all the messages in a particular ticket

```javascript
socket.emit('get_ticket_messages', {
    ticket_id: "ID of the ticket the message is coming from",
    product: "The Product name",
    workspace_id: "Your workspace ID",
    api_key: "Your ApI Key",
});
```

#### Client Listening:
```javascript
socket.on('ticket_message_response', (data) => {
    // Handle response for the event
    console.log(data);
});
```

### ```Create Ticket```
This event is used to create a new ticket 

```javascript
socket.emit('create_ticket', {
    user_id: "Public user id of the creator",
    product: "The Product name",
    workspace_id: "Your workspace ID",
    api_key: "Your ApI Key",
    created_at: "Date of Creation"
});
```

#### Client Listening:
```javascript
socket.on('ticket_response', (data) => {
    // Handle response for the event
    console.log(data);
});
```

### ```Get  Tickets ```
This event returns all the tickets in a particular product

```javascript
socket.emit('get_tickets', {
    product: "The Product name",
    workspace_id: "Your workspace ID",
    api_key: "Your ApI Key",
});
```

#### Client Listening:
```javascript
socket.on('ticket_response', (data) => {
    // Handle response for the event
    console.log(data);
});
```

### ```Close  Ticket ```
This event closes a tickets in a particular product

```javascript
socket.emit('close_ticket', {
    ticket_id: "ID of the ticket to be closed",
    line_manager: "ID of the line manager that is assigned to the ticket",
    product: "The Product name",
    workspace_id: "Your workspace ID",
    api_key: "Your ApI Key",
});
```

#### Client Listening:
```javascript
socket.on('ticket_response', (data) => {
    // Handle response for the event
    console.log(data);
});
```