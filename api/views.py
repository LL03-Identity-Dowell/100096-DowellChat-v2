async_mode = 'gevent'
# async_mode = "threading"
from django.shortcuts import redirect, render
import requests
from .models import Message
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .serializers import MessageSerializer
from .utils import *
import os
import json
from django.http import HttpResponse
import socketio
import base64
from datetime import date
from django.conf import settings

from .kafka_producer import ProducerTicketChat
import random
import re


sio = socketio.Server(cors_allowed_origins=[
    'http://localhost:5000',
    'https://admin.socket.io',
    "*"], 
    async_mode=async_mode)
sio.instrument(auth={
    'username': 'admin',
    'password': os.getenv("ADMIN_PASSWORD"),
})
app = socketio.WSGIApp(sio)
thread = None

my_api_key = os.getenv("API_KEY")
if my_api_key is None:
    raise ValueError("API_KEY is missing. Make sure it is set in the .env file.")
data_cube = DataCubeConnection()

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


"""SERVER EVENT SECTION"""

@sio.event
def get_user_servers(sid, message):
    try:
        user_id = message['user_id']
        workspace_id = message['workspace_id']
        api_key = message['api_key']
        product = message['product']

        db_name = f"{workspace_id}_{product}"
        coll_name = f"{workspace_id}_server"

        if not check_db(workspace_id):
            return sio.emit('server_response', {'data':"No DB found for the Workspace", 'status': 'failure', 'operation':'get_user_servers'}, room=sid)

        if check_collection(workspace_id, "server"):

            if product == "customer_support":
                response = data_cube.fetch_data(
                    api_key=api_key,
                    db_name=db_name,
                    coll_name=coll_name,
                    filters={},
                    limit=199,
                    offset=0
                )
            else:
                response = data_cube.fetch_data(
                    api_key=api_key,
                    db_name=db_name,
                    coll_name=coll_name,
                    filters={"$or": [{"owner": user_id}, {"member_list": {"$in": [user_id]}}]},
                    limit=199,
                    offset=0
                )

            if response['success']:
                if not response['data']:
                    return sio.emit('server_response', {'data': 'No Server found for this User', 'status': 'failure', 'operation': 'get_user_servers'}, room=sid)

                else:
                    servers = []
                    for server in response['data']:
                        servers.append({'name': server['name'], 'id': str(server['_id'])})

                    return sio.emit('server_response', {'data': servers, 'status': 'success', 'operation': 'get_user_servers'}, room=sid)
            else:
                # Error in fetching data
                return sio.emit('server_response', {'data': response['message'], 'status': 'failure', 'operation': 'get_user_servers'}, room=sid)

    except Exception as e:
        # Handle other exceptions
        error_message = str(e)
        return sio.emit('channel_response', {'data': error_message, 'status': 'failure', 'operation': 'get_user_servers'}, room=sid)


@sio.event
def create_server(sid, message):
    """Create a new server."""
    try:
        workspace_id = message['workspace_id']
        api_key = message['api_key']
        product = message['product']
        name = message['name']
        member_list = message['member_list']
        channels = message['channels']
        events = message['events'] 
        owner = message['owner']
        created_at = message['created_at']
        
        data = {
                "name": name,
                "member_list": member_list,
                "channels": channels,
                "events": events,
                "owner": owner,
                "created_at": created_at, 
        }
        
        db_name = f"{workspace_id}_{product}"
        coll_name = f"{workspace_id}_server"

        if not check_db(workspace_id):
            return sio.emit('server_response', {'data':"No DB found for the Workspace", 'status': 'failure', 'operation':'create_server'}, room=sid)
        if check_collection(workspace_id, "server"):
            response = data_cube.insert_data(api_key=api_key, db_name=db_name, coll_name=coll_name, data=data)

            if response['success'] == True:
                return sio.emit('server_response', {'data':response['data'], 'status': 'success', 'operation':'create_server'}, room=sid)
            else:
                return sio.emit('server_response', {'data':response['message'], 'status': 'failure', 'operation':'create_server'}, room=sid)
    except Exception as e:
        # Handle other exceptions
        error_message = str(e)
        return sio.emit('server_response', {'data': error_message, 'status': 'failure', 'operation':'create_server'}, room=sid)
  
@sio.event
def get_server(sid, message):
    try:
        server_id = message['server_id']
        workspace_id = message['workspace_id']
        api_key = message['api_key']
        product = message['product']

        db_name = f"{workspace_id}_{product}"
        coll_name = f"{workspace_id}_server"

        response = data_cube.fetch_data(api_key=api_key, db_name=db_name, coll_name=coll_name, filters={"_id": server_id}, limit=1, offset=0)

        if response['success']:
            if response['data']:
                # Record found
                server_data = response['data'][0]
                return sio.emit('server_response', {'data': server_data, 'status': 'success', 'operation':'get_server'}, room=sid)
            else:
                # No record found
                return sio.emit('server_response', {'data': 'No data found for this query', 'status': 'success', 'operation':'get_server'}, room=sid)
        else:
            # Error in fetching data
            return sio.emit('server_response', {'data': response['message'], 'status': 'failure', 'operation':'get_server'}, room=sid)

    except Exception as e:
        # Handle other exceptions
        error_message = str(e)
        return sio.emit('server_response', {'data': error_message, 'status': 'failure', 'operation':'get_server'}, room=sid)
    

@sio.event
def update_server(sid, message):
    try:
        server_id = message['server_id']
        server_name = message['name']
        # member_list = message['member_list']
        # channels = message['channels']
        # events = message['events'] 
        
        workspace_id = message['workspace_id']
        api_key = message['api_key']
        product = message['product']

        db_name = f"{workspace_id}_{product}"
        coll_name = f"{workspace_id}_server"


        update_data = {
                "name": server_name,
                # "member_list": member_list,
                # "channels": channels,
                # "events": events,

        }

        response = data_cube.update_data(api_key=api_key,db_name=db_name, coll_name=coll_name, query = {"_id": server_id}, update_data=update_data)    
        if response['success'] == True:
            return sio.emit('server_response', {'data':"Server Updated Successfully", 'status': 'success', 'operation':'update_server'}, room=sid)
        else:
            return sio.emit('server_response', {'data':"Error updating server", 'status': 'failure', 'operation':'update_server'}, room=sid)
    except Exception as e:
        error_message = str(e)
        return sio.emit('server_response', {'data': error_message, 'status': 'failure', 'operation':'update_server'}, room=sid)


@sio.event
def delete_server(sid, message):
    try:
        server_id = message['server_id']
        
        workspace_id = message['workspace_id']
        api_key = message['api_key']
        product = message['product']

        db_name = f"{workspace_id}_{product}"
        coll_name = f"{workspace_id}_server"

        response = data_cube.delete_data(api_key=api_key,db_name=db_name, coll_name=coll_name, query={"_id": server_id})

        if response['success']:
            if response['message']:
                return sio.emit('server_response', {'data': "Server Deleted Successfully", 'status': 'success', 'operation':'delete_server'}, room=sid)
            else:
                return sio.emit('server_response', {'data': 'No data found for this query', 'status': 'success', 'operation':'delete_server'}, room=sid)
        else:
            return sio.emit('server_response', {'data': response['message'], 'status': 'failure', 'operation':'delete_server'}, room=sid)

    except Exception as e:
        error_message = str(e)
        return sio.emit('server_response', {'data': error_message, 'status': 'failure', 'operation':'delete_server'}, room=sid)

@sio.event
def add_server_member(sid, message):
    try:
        server_id = message['server_id']
        user_id = message['user_id']
        
        workspace_id = message['workspace_id']
        api_key = message['api_key']
        product = message['product']

        db_name = f"{workspace_id}_{product}"
        coll_name = f"{workspace_id}_server"
        # Fetch the server details
        server_data = data_cube.fetch_data(api_key=api_key,db_name=db_name, coll_name=coll_name, filters={"_id": server_id}, limit=1, offset=0)

        if not server_data['data']:
            return sio.emit('server_response', {'data': 'Server not found', 'status': 'failure', 'operation': 'add_server_member'}, room=sid)

        server = server_data['data'][0]

        # Update the server's member_list
        existing_member_list = server.get('member_list', [])
        if user_id not in existing_member_list:
            updated_member_list = existing_member_list + [user_id]
            update_data = {
                "member_list": updated_member_list,
            }
            response = data_cube.update_data(api_key=api_key, db_name=db_name, coll_name=coll_name, query={"_id": server_id}, update_data=update_data)

            if not response['success']:
                return sio.emit('server_response', {'data': "Error adding user to server", 'status': 'failure', 'operation': 'add_server_member'}, room=sid)

        if product =="dowellchat":
            # Fetch the channels associated with the server
            channels_data = data_cube.fetch_data(api_key=api_key, db_name=db_name, coll_name=f"{workspace_id}_channel", filters={"server": server_id}, limit=199, offset=0)
            channels = channels_data['data']
            
            user_added_to_channel = False

            for channel in channels:
                # Check if the channel is private
                private_value = channel.get('private', '').upper().strip()
                print(f"Private value: '{private_value}', Length: {len(private_value)}")

                # If the channel is not private, add the member to the channel
                if private_value == 'false':
                    print("Entered")
                    existing_member_list = channel.get('member_list', [])
                    print(existing_member_list)

                    if user_id in existing_member_list:
                        print('User is already a member of this channel')
                        continue  # Move to the next channel

                    updated_member_list = existing_member_list + [user_id]
                    update_data = {
                        "member_list": updated_member_list,
                    }
                    response = data_cube.update_data(api_key=api_key, db_name=db_name, coll_name=f"{workspace_id}_channel", query={"_id": channel['_id']}, update_data=update_data)

                    if response['success']:
                        print('User added successfully to channel')
                        user_added_to_channel = True

        else:
            user_added_to_channel = True

        # Check if the user was added to at least one channel
        if user_added_to_channel:
            return sio.emit('server_response', {'data': "User added to the Server and at least one channel", 'status': 'success', 'operation': 'add_channel_member'}, room=sid)
        else:
            return sio.emit('server_response', {'data': "User is already a member in all channels or an error occurred", 'status': 'failure', 'operation': 'add_channel_member'}, room=sid)
    except Exception as e:
        error_message = str(e)
        return sio.emit('server_response', {'data': error_message, 'status': 'failure', 'operation': 'add_server_member'}, room=sid)


@sio.event
def delete_server_member(sid, message):
    try:
        server_id = message['server_id']
        user_id = message['user_id']

        workspace_id = message['workspace_id']
        api_key = message['api_key']
        product = message['product']

        db_name = f"{workspace_id}_{product}"
        coll_name = f"{workspace_id}_server"

        server_data = data_cube.fetch_data(api_key=api_key,db_name=db_name, coll_name=coll_name, filters={"_id": server_id}, limit=1, offset=0)

        if not server_data['data']:
            return sio.emit('server_response', {'data': 'Server not found', 'status': 'failure', 'operation': 'remove_server_member'}, room=sid)

        # Delete the user from the server's member list
        existing_member_list = server_data['data'][0].get('member_list', [])
        updated_member_list = [member for member in existing_member_list if member != user_id]

        update_data = {
            "member_list": updated_member_list,
        }

        response = data_cube.update_data(api_key=api_key,db_name=db_name, coll_name=coll_name, query={"_id": server_id}, update_data=update_data)

        if not response['success']:
            return sio.emit('server_response', {'data': "Error removing user from Server", 'status': 'failure', 'operation': 'remove_server_member'}, room=sid)

        if product =="dowellchat":
            # Fetch the channels associated with the server
            channels_data = data_cube.fetch_data(db_name="dowellchat", coll_name="channel", filters={"server": server_id}, limit=199, offset=0)
            channels = channels_data['data']

            user_removed_from_channel = False

            for channel in channels:
                # Update the channel's member list
                existing_member_list = channel.get('member_list', [])
                updated_member_list = [member for member in existing_member_list if member != user_id]

                update_data = {
                    "member_list": updated_member_list,
                }

                response = data_cube.update_data(db_name="dowellchat", coll_name="channel", query={"_id": channel['_id']}, update_data=update_data)

                if response['success']:
                    user_removed_from_channel = True
        else:
            user_removed_from_channel = True

        if user_removed_from_channel:
            return sio.emit('server_response', {'data': "User removed from Server and all channels", 'status': 'success', 'operation': 'remove_server_member'}, room=sid)
        else:
            return sio.emit('server_response', {'data': "User removed from Server only or an error occurred", 'status': 'failure', 'operation': 'remove_server_member'}, room=sid)

    except Exception as e:
        error_message = str(e)
        return sio.emit('server_response', {'data': error_message, 'status': 'failure', 'operation': 'remove_server_member'}, room=sid)


"""CHANNEL EVENT SECTION"""
@sio.event
def create_channel(sid, message):
    try:
        name = message['name']
        topic = message['topic']
        channel_type = message['type']
        private = message['private'] 
        server = message['server']
        member_list = message['member_list']
        created_at = message['created_at']

        data = {
                "name": name,
                "topic": topic,
                "type": channel_type,
                "private": private,
                "member_list": member_list,
                "server":server,        
                "created_at": created_at, 
        }
        is_server = data_cube.fetch_data(db_name="dowellchat", coll_name="server", filters={"_id": server}, limit=1, offset=0)

        if is_server['data'] ==[]:
            return sio.emit('channel_response', {'data': 'Server not found', 'status': 'failure', 'operation':'create_channel'}, room=sid)
            
        response = data_cube.insert_data(db_name="dowellchat", coll_name="channel", data=data)
        
        if response['success'] == True:
            channels = data_cube.fetch_data(db_name="dowellchat", coll_name="channel", filters={"server": server}, limit=199, offset=0)
            channel_list=[]
            for channel in channels['data']:
                channel_list.append(channel['name'])
            sio.emit('channel_response', {'data': channel_list, 'status': 'success', 'operation':'get_server_channels'}, room=sid)    
            sio.enter_room(sid, name)
            return sio.emit('channel_response', {'data':"Channel Created Successfully", 'status': 'success', 'operation':'create_channel'}, room=sid)
        
        else:
            return sio.emit('channel_response', {'data':"Error creating Channel", 'status': 'failure', 'operation':'create_channel'}, room=sid)
    except Exception as e:
        # Handle other exceptions
        error_message = str(e)
        return sio.emit('channel_response', {'data': error_message, 'status': 'failure', 'operation':'create_channel'}, room=sid)

@sio.event
def get_server_channels(sid, message):
    try:
        server_id = message['server_id']
        response = data_cube.fetch_data(db_name="dowellchat", coll_name="channel", filters={"server": server_id}, limit=199, offset=0)
        if response['success']:
            if not response['data']:
                return sio.emit('channel_response', {'data': 'No Channel found for this Server', 'status': 'failure', 'operation':'get_server_channels'}, room=sid)

            else:
                channels=[]
                for channel in response['data']:
                    channels.append(channel['name'])
                return sio.emit('channel_response', {'data': channels, 'status': 'success', 'operation':'get_server_channels'}, room=sid)
        else:
            return sio.emit('channel_response', {'data': response['message'], 'status': 'failure', 'operation':'get_server_channels'}, room=sid)

    except Exception as e:
        error_message = str(e)
        return sio.emit('channel_response', {'data': error_message, 'status': 'failure', 'operation':'get_server_channels'}, room=sid)

@sio.event
def update_channel(sid, message):
    try:
        channel_id = message['channel_id']
        name = message['name']
        topic = message['topic']
        private = message['private'] 

        update_data = {
                "name": name,
                "topic": topic,
                "private": private,
        }

        response = data_cube.update_data(db_name="dowellchat", coll_name="channel", query = {"_id": channel_id}, update_data=update_data)     
        
        if response['success'] == True:
            return sio.emit('channel_response', {'data':"Channel Updated Successfully", 'status': 'success', 'operation':'update_channel'}, room=sid)
        else:
            return sio.emit('channel_response', {'data':"Error updating Channel", 'status': 'failure', 'operation':'update_channel'}, room=sid)
    except Exception as e:
        # Handle other exceptions
        error_message = str(e)
        return sio.emit('channel_response', {'data': error_message, 'status': 'failure', 'operation':'update_channel'}, room=sid)

@sio.event
def delete_channel(sid, message):
    try:
        channel_id = message['channel_id']
        response = data_cube.delete_data(db_name="dowellchat", coll_name="channel", query={"_id": channel_id})

        if response['success']:
            if response['message']:
                return sio.emit('channel_response', {'data': "Channel Deleted Successfully", 'status': 'success', 'operation':'delete_channel'}, room=sid)
            else:
                return sio.emit('channel_response', {'data': 'No data found for this query', 'status': 'success', 'operation':'delete_channel'}, room=sid)
        else:
            return sio.emit('channel_response', {'data': response['message'], 'status': 'failure', 'operation':'delete_channel'}, room=sid)

    except Exception as e:
        error_message = str(e)
        return sio.emit('channel_response', {'data': error_message, 'status': 'failure', 'operation':'delete_channel'}, room=sid)
    
@sio.event
def add_channel_member(sid, message):
    try:
        channel_id = message['channel_id']
        user_id = message['user_id']

        is_channel = data_cube.fetch_data(db_name="dowellchat", coll_name="channel", filters={"_id": channel_id}, limit=1, offset=0)

        if not is_channel['data']:
            return sio.emit('channel_response', {'data': 'Channel not found', 'status': 'failure', 'operation': 'add_channel_member'}, room=sid)

        existing_member_list = is_channel['data'][0].get('member_list', [])

        # Check if user_id is already in the member_list
        if user_id in existing_member_list:
            return sio.emit('channel_response', {'data': 'User is already a member', 'status': 'failure', 'operation': 'add_channel_member'}, room=sid)

        # Add the user_id to the member_list
        updated_member_list = existing_member_list + [user_id]
        update_data = {
            "member_list": updated_member_list,
        }

        response = data_cube.update_data(db_name="dowellchat", coll_name="channel", query={"_id": channel_id}, update_data=update_data)

        if response['success']:
            return sio.emit('channel_response', {'data': "User added Successfully", 'status': 'success', 'operation': 'add_channel_member'}, room=sid)
        else:
            return sio.emit('channel_response', {'data': "Error adding user", 'status': 'failure', 'operation': 'add_channel_member'}, room=sid)

    except Exception as e:
        error_message = str(e)
        return sio.emit('channel_response', {'data': error_message, 'status': 'failure', 'operation': 'add_channel_member'}, room=sid)

@sio.event
def delete_channel_member(sid, message):
    try:
        channel_id = message['channel_id']
        user_id = message['user_id']
        is_channel = data_cube.fetch_data(db_name="dowellchat", coll_name="channel", filters={"_id": channel_id}, limit=1, offset=0)

        if not is_channel['data']:
            return sio.emit('channel_response', {'data': 'Channel not found', 'status': 'failure', 'operation': 'remove_channel_member'}, room=sid)
        existing_member_list = is_channel['data'][0].get('member_list', [])
        updated_member_list = [member for member in existing_member_list if member != user_id]

        update_data = {
            "member_list": updated_member_list,
        }

        response = data_cube.update_data(db_name="dowellchat", coll_name="channel", query={"_id": channel_id}, update_data=update_data)

        if response['success']:
            return sio.emit('channel_response', {'data': "User Removed Successfully", 'status': 'success', 'operation': 'remove_channel_member'}, room=sid)
        else:
            return sio.emit('channel_response', {'data': "Error removing user from Channel", 'status': 'failure', 'operation': 'remove_channel_member'}, room=sid)

    except Exception as e:
        error_message = str(e)
        return sio.emit('channel_response', {'data': error_message, 'status': 'failure', 'operation': 'remove_channel_member'}, room=sid)


"""CATEGORY EVENT SECTION"""
@sio.event
def create_category(sid, message):
    try:
        name = message['name']
        server = message['server_id']
        private = message['private']
        created_at = message['created_at']

        data = {
                "name": name,
                "server":server,
                "private": private,        
                "created_at": created_at, 
        }
        is_server = data_cube.fetch_data(db_name="dowellchat", coll_name="server", filters={"_id": server}, limit=1, offset=0)

        if is_server['data'] ==[]:
            return sio.emit('category_response', {'data': 'Server not found', 'status': 'failure', 'operation':'create_category'}, room=sid)
            
        response = data_cube.insert_data(db_name="dowellchat", coll_name="category", data=data)
        
        if response['success'] == True:
            return sio.emit('category_response', {'data':"Category Created Successfully", 'status': 'success', 'operation':'create_category'}, room=sid)
        
        else:
            return sio.emit('category_response', {'data':"Error creating Category", 'status': 'failure', 'operation':'create_category'}, room=sid)
    except Exception as e:
        # Handle other exceptions
        error_message = str(e)
        return sio.emit('category_response', {'data': error_message, 'status': 'failure', 'operation':'create_category'}, room=sid)


@sio.event
def update_category(sid, message):
    try:
        category_id = message['category_id']
        name = message['name']
        private = message['private'] 

        update_data = {
                "name": name,
                "private": private,
        }

        response = data_cube.update_data(db_name="dowellchat", coll_name="category", query = {"_id": category_id}, update_data=update_data)     
        
        if response['success'] == True:
            return sio.emit('category_response', {'data':"Category Updated Successfully", 'status': 'success', 'operation':'update_category'}, room=sid)
        else:
            return sio.emit('category_response', {'data':"Error updating Category", 'status': 'failure', 'operation':'update_category'}, room=sid)
    except Exception as e:
        # Handle other exceptions
        error_message = str(e)
        return sio.emit('category_response', {'data': error_message, 'status': 'failure', 'operation':'update_category'}, room=sid)

@sio.event
def delete_category(sid, message):
    try:
        category_id = message['category_id']
        response = data_cube.delete_data(db_name="dowellchat", coll_name="category", query={"_id": category_id})

        if response['success']:
            if response['message']:
                return sio.emit('category_response', {'data': "Category Deleted Successfully", 'status': 'success', 'operation':'delete_category'}, room=sid)
            else:
                return sio.emit('category_response', {'data': 'No data found for this query', 'status': 'success', 'operation':'delete_category'}, room=sid)
        else:
            return sio.emit('category_response', {'data': response['message'], 'status': 'failure', 'operation':'delete_category'}, room=sid)

    except Exception as e:
        error_message = str(e)
        return sio.emit('category_response', {'data': error_message, 'status': 'failure', 'operation':'delete_category'}, room=sid)



"""EVENT EVENT SECTION"""


def emit_response(sid, event, data, status, operation):
    sio.emit(event, {
        'data': data,
        'status': status,
        'operation': operation
    }, room=sid)


@sio.event
def create_event(sid, message):
    try:
        topic = message['topic']
        start_date = message['start_date']
        start_time = message['start_time']
        description = message['description']
        location = message['location']
        server = message['server']
        created_at = message['created_at']

        data = {
                "topic": topic,
                "start_date": start_date,
                "start_time": start_time,
                "description": description,
                "location": location, 
                "server":server,
                "created_at": created_at, 
        }
        is_server = data_cube.fetch_data(db_name="dowellchat", coll_name="server", filters={"_id": server}, limit=1, offset=0)

        if is_server['data'] ==[]:
            return emit_response(sid, "event_response", "Server not found", 'failure', 'create_event')
            
        response = data_cube.insert_data(db_name="dowellchat", coll_name="events", data=data)
        
        print(response)
        if response['success'] == True:
            return emit_response(sid, "event_response", "Event Created Successfully", 'success', 'create_event')
        
        else:
            return emit_response(sid, "event_response", "Error creating event", 'failure', 'create_event')

    except Exception as e:
        return emit_response(sid, "event_response", str(e), 'failure', 'create_event')


@sio.event
def get_server_events(sid, message):
    try:
        server_id = message['server_id']
        response = data_cube.fetch_data(db_name="dowellchat", coll_name="events", filters={"server": server_id}, limit=199, offset=0)
        if response['success']:
            if not response['data']:
                return emit_response(sid, "event_response", "No Event found for this Server", "failure", "get_server_events")

            else:
                return emit_response(sid, "event_response", response['data'], "success", "get_server_events")

        else:
            return emit_response(sid, "event_response", response['message'], "failure", "get_server_events")

    except Exception as e:
        error_message = str(e)
        return emit_response(sid, "event_response", error_message, "failure", "get_server_events")

@sio.event
def get_event_details(sid, message):
    try:
        event_id = message['event_id']
        response = data_cube.fetch_data(db_name="dowellchat", coll_name="events", filters={"_id": event_id}, limit=199, offset=0)
        if response['success']:
            if not response['data']:
                return emit_response(sid, "event_response", "No Event found", "failure", "get_event_details")
            else:
                return emit_response(sid, "event_response", response['data'], "success", "get_event_details")
        else:
            return emit_response(sid, "event_response", response['message'], "failure", "get_event_events")

    except Exception as e:
        error_message = str(e)
        return emit_response(sid, "event_response", error_message, "failure", "get_event_events")

@sio.event
def update_event(sid, message):
    try:
        event_id = message['event_id']
        topic = message['topic']
        start_date = message['start_date']
        start_time = message['start_time']
        description = message['description']
        location = message['location']

        update_data = {
                "topic": topic,
                "start_date": start_date,
                "start_time": start_time,
                "description": description,
                "location": location, 
        }

        response = data_cube.update_data(db_name="dowellchat", coll_name="events", query = {"_id": event_id}, update_data=update_data)     
        print(response)
        if response['success'] == True:
            return emit_response(sid, "event_response", "Event Updated Successfully", "success", "update_event")
        else:
            return emit_response(sid, "event_response", "Error updating event", 'failure', 'update_event')
    except Exception as e:
        # Handle other exceptions
        error_message = str(e)
        return emit_response(sid, "event_response", error_message, "failure", "update_event")


@sio.event
def cancel_event(sid, message):
    try:
        event_id = message['event_id']
        response = data_cube.delete_data(db_name="dowellchat", coll_name="events", query={"_id": event_id})

        if response['success']:
            if response['message']:
                return emit_response(sid, "event_response", "Event Cancelled Successfully", "success", "cancel_event")
            else:
                return emit_response(sid, "event_response", "No data found for this query", "failure", "cancel_event")
        else:
            return emit_response(sid, "event_response", response['message'], "failure", "cancel_event")
            

    except Exception as e:
        error_message = str(e)
        return emit_response(sid, "event_response", error_message, "failure", "cancel_event")


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

@sio.event
def endCall(sid):
    sio.emit('callEnded')


"""CHANNEL CHAT SECTION"""
@sio.event
def auto_join_channel_chat(sid, message):
    user_id = message['user_id']

    # Check if the user is connected
    if sid:
        response = data_cube.fetch_data(db_name="dowellchat", coll_name="channel", filters={"member_list": {"$in": [user_id]}}, limit=199, offset=0)

        if response['success']:
            for channel in response['data']:
                channel_id = str(channel['_id'])

                # Make the user join the room
                sio.enter_room(sid, channel_id)
                             
                
@sio.event
def join_channel_chat(sid, message):
    try:
        channel_id = message['channel_id']
        workspace_id = message['workspace_id']
        api_key = message['api_key']
        product = message['product']

        db_name = f"{workspace_id}_{product}"
        coll_name = f"{workspace_id}_channel"
        
        response = data_cube.fetch_data(api_key=api_key,db_name=db_name, coll_name=coll_name, filters={"_id": channel_id}, limit=1, offset=0)

        if response['success']:
            if not response['data']:
                return sio.emit('channel_chat_response', {'data': 'No Channel found ', 'status': 'failure', 'operation':'join_channel_chat'}, room=sid)
            else:
                sio.enter_room(sid, channel_id)
                msg_response = data_cube.fetch_data(api_key=api_key,db_name=db_name, coll_name=f"{workspace_id}_channel_chat", filters={"channel_id": channel_id}, limit=200, offset=0)
                if msg_response['data']:
                    sio.emit('channel_chat_response', {'data': msg_response['data'], 'status': 'success', 'operation': 'join_channel_chat'}, room=sid)
                    
                    #Mark the messages as read
                    update_data = {
                        'is_read': True, 
                    }
                    mark_read = data_cube.update_data(api_key=my_api_key, db_name=db_name, coll_name=f"{workspace_id}_channel_chat", query={"channel_id": channel_id}, update_data=update_data)
                else:
                    sio.emit('channel_chat_response', {'data': [], 'status': 'success', 'operation': 'join_channel_chat'}, room=sid)    
                return
                
    except Exception as e:
        error_message = str(e)
        return sio.emit('channel_chat_response', {'data': error_message, 'status': 'failure'}, room=channel_id)

@sio.event
def channel_message_event(sid, message):
    try:
        channel_id = message['channel_id']
        message_data = message.get('message_data', None)
        file_data = message.get('file',None) 
        user_id = message['user_id']
        name = message['name']
        reply_to = message['reply_to']
        created_at = message['created_at']

        workspace_id = message['workspace_id']
        api_key = message['api_key']
        product = message['product']
        
        db_name = f"{workspace_id}_{product}"
        coll_name = f"{workspace_id}_channel_chat"


        print(file_data)
        print("Checkpoint 0")
        # Handling file upload
        file_path = None
        if file_data['content'] != None and file_data['filename'] != None:
            try:
                print("Checkpoint 1")
                # Decode base64 and sanitize the file name
                file_content = base64.b64decode(file_data['content'])
                sanitized_filename = sanitize_filename(file_data['filename'])
                timestamp = get_safe_timestamp()
                file_name = f"{user_id}_{timestamp}_{sanitized_filename}"  
                file_path = os.path.join('media', file_name)

                with open(file_path, 'wb') as file:
                    file.write(file_content)

                file_path = f"{settings.ENDPOINT_URL}\{file_path}"
            
                
            except Exception as e:
                print(str(e))
                return sio.emit('channel_chat_response', {'data': f"Error saving file: {str(e)}", 'status': 'failure'}, room=sid)
        else:
            if message_data == None or message_data == "":
                return sio.emit('channel_chat_response', {'data': f"Error sending message: Please provide message_data or attach a file", 'status': 'failure'}, room=sid)

        data = {
            "channel_id": channel_id,
            "message_data": message_data,
            "file": file_path,
            "author": {
                "user_id": user_id,
                "name": name
            },
            "reply_to": reply_to,
            "is_read": False,
            "created_at": created_at,
        }
        

        response = data_cube.insert_data(api_key=api_key,db_name=db_name, coll_name=coll_name, data=data)

        if response['success']:
            return sio.emit('channel_chat_response', {'data': data, 'status': 'success'}, room=sid)
        else:
            return sio.emit('channel_chat_response', {'data': "Error sending message", 'status': 'failure'}, room=sid)
    except Exception as e:
        error_message = str(e)
        return sio.emit('channel_chat_response', {'data': error_message, 'status': 'failure'}, room=sid)
    
"""CUSTOMER SUPPORT SECTION"""
@sio.event
def cs_create_category(sid, message):
    try:
        name = message['name']
        server = message['server_id']
        member_list = message['member_list']
        rooms= message['rooms']
        private = message['private']
        created_at = message['created_at']

        workspace_id = message['workspace_id']
        api_key = message['api_key']
        product = message['product']

        db_name = f"{workspace_id}_{product}"
        coll_name = f"{workspace_id}_category"

        data = {
                "name": name,
                "rooms": rooms,
                "server_id":server,
                "member_list":member_list,
                "private": private,        
                "created_at": created_at, 
        }

        is_server = data_cube.fetch_data(api_key=api_key,db_name=db_name, coll_name=f"{workspace_id}_server", filters={"_id": server}, limit=1, offset=0)

        if is_server['data'] ==[]:
            return sio.emit('category_response', {'data': 'Server not found', 'status': 'failure', 'operation':'create_category'}, room=sid)

        if check_collection(workspace_id, "category"):
                
            response = data_cube.insert_data(api_key=api_key,db_name=db_name, coll_name=coll_name, data=data)
            
            if response['success'] == True:
                sio.enter_room(sid, response['data']['inserted_id'])
                return sio.emit('category_response', {'data':response['data'], 'status': 'success', 'operation':'create_category'}, room=sid)

            else:
                return sio.emit('category_response', {'data':"Error creating Category", 'status': 'failure', 'operation':'create_category'}, room=sid)
    except Exception as e:
        # Handle other exceptions
        error_message = str(e)
        return sio.emit('category_response', {'data': error_message, 'status': 'failure', 'operation':'create_category'}, room=sid)


@sio.event
def cs_get_server_category(sid, message):
    try:
        server_id = message['server_id']
        workspace_id = message['workspace_id']
        api_key = message['api_key']
        product = message['product']

        db_name = f"{workspace_id}_{product}"
        coll_name = f"{workspace_id}_category"

        if check_collection(workspace_id, "category"):
            response = data_cube.fetch_data(api_key=api_key,db_name=db_name, coll_name=coll_name, filters={"server_id": server_id}, limit=199, offset=0)
            if response['success']:
                if not response['data']:
                    return sio.emit('category_response', {'data': 'No Category found for this Server', 'status': 'failure', 'operation':'get_server_category'}, room=sid)

                else:
                    formatted_response = []

                    for category in response['data']:
                        category_name = category.get('_id', '')
                        
                        rooms_details = get_room_details(workspace_id, api_key, product, category_name)
                        
                        formatted_category = {
                            "_id": category['_id'],
                            "name": category['name'],
                            "rooms": rooms_details,
                            "server_id": category['server_id'],
                            "member_list": category['member_list'],
                            "private": category['private'],
                            "created_at": category['created_at']
                        }

                        formatted_response.append(formatted_category)

                        if category_name:
                            sio.enter_room(sid, category_name)

                        
                    
                    return sio.emit('category_response', {'data': formatted_response, 'status': 'success', 'operation':'get_server_category'}, room=sid)
            else:
                return sio.emit('category_response', {'data': response['message'], 'status': 'failure', 'operation':'get_server_category'}, room=sid)

    except Exception as e:
        error_message = str(e)
        return sio.emit('category_response', {'data': error_message, 'status': 'failure', 'operation':'get_server_category'}, room=sid)


@sio.event
def cs_get_user_category(sid, message):
    try:
        server_id = message['server_id']
        user_id = message['user_id']

        workspace_id = message['workspace_id']
        api_key = message['api_key']
        product = message['product']

        db_name = f"{workspace_id}_{product}"
        coll_name = f"{workspace_id}_category"       
        
         # Query based on owner
        response_owner = data_cube.fetch_data(
            api_key=api_key,
            db_name=db_name,
            coll_name=f"{workspace_id}_server",
            filters={"owner": user_id},
            limit=1,
            offset=0
        )

        # Query based on _id
        response_id = data_cube.fetch_data(
            api_key=api_key,
            db_name=db_name,
            coll_name=f"{workspace_id}_server",
            filters={"_id": server_id},
            limit=1,
            offset=0
        )
        
        if response_owner['success'] and response_owner['data'] and response_id['success'] and response_id['data']:
            if check_collection(workspace_id, "category"):
                new_response = data_cube.fetch_data(
                    api_key=api_key,
                    db_name=db_name,
                    coll_name=coll_name, 
                    filters={"server_id": server_id}, 
                    limit=199, 
                    offset=0
                )

                if new_response['success']:
                    if new_response['data']:
                        # Emit the category response to the customer support personnel
                        sio.emit('category_response', {'data': new_response['data'], 'status': 'success',
                                                       'operation': 'get_user_category'}, room=sid)

                        # Join the rooms named after each category
                        for category in new_response['data']:
                            category_name = category.get('_id', '')
                            if category_name:
                                sio.enter_room(sid, category_name)

                               
                        return

        if check_collection(workspace_id, "category"):
            new_response = data_cube.fetch_data(
                api_key=api_key,
                db_name=db_name,
                coll_name=coll_name, 
                filters={"$and": [{"server_id": server_id}, {"member_list": {"$in": [user_id]}}]},  
                limit=199, 
                offset=0
                )
            if new_response['success']:
                    if new_response['data']:
                         # Emit the category response to the customer support personnel
                        sio.emit('category_response', {'data': new_response['data'], 'status': 'success',
                                                    'operation': 'get_user_category'}, room=sid)

                        # Join the rooms named after each category
                        for category in new_response['data']:
                            category_name = category.get('_id', '')
                            if category_name:
                                sio.enter_room(sid, category_name)

                                # Add more logic here if needed for handling new category rooms
                        return

            else:
                return sio.emit('category_response', {'data': new_response['message'], 'status': 'failure', 'operation':'get_user_category'}, room=sid)

            return sio.emit('category_response', {'data': "No category found", 'status': 'failure', 'operation':'get_user_category'}, room=sid)
    
    except Exception as e:
        error_message = str(e)
        return sio.emit('category_response', {'data': error_message, 'status': 'failure', 'operation':'get_user_category'}, room=sid)


@sio.event
def cs_get_category_room(sid, message):
    try:
        category_id = message['category_id']
        workspace_id = message['workspace_id']
        api_key = message['api_key']
        product = message['product']

        db_name = f"{workspace_id}_{product}"
        coll_name = f"{workspace_id}_public_room"

        if check_collection(workspace_id, "category"):
            response = data_cube.fetch_data(api_key=api_key,db_name=db_name, coll_name=coll_name, filters={"category": category_id}, limit=20, offset=0)
            if response['success']:
                if not response['data']:
                    return sio.emit('category_response', {'data': 'No Room found for this Category', 'status': 'failure', 'operation':'get_category_room'}, room=sid)

                else:
                    return sio.emit('category_response', {'data': response['data'], 'status': 'success', 'operation':'get_category_room'}, room=sid)
            else:
                return sio.emit('category_response', {'data': response['message'], 'status': 'failure', 'operation':'get_category_room'}, room=sid)

    except Exception as e:
        error_message = str(e)
        return sio.emit('category_response', {'data': error_message, 'status': 'failure', 'operation':'get_category_room'}, room=sid)

@sio.event
def cs_update_category(sid, message):
    try:

        category_id = message['category_id']
        name = message['name']
        private = message['private'] 

        workspace_id = message['workspace_id']
        api_key = message['api_key']
        product = message['product']

        db_name = f"{workspace_id}_{product}"
        coll_name = f"{workspace_id}_category"       


        update_data = {
                "name": name,
                "private": private,
        }

        response = data_cube.update_data(api_key=api_key, db_name=db_name, coll_name=coll_name, query = {"_id": category_id}, update_data=update_data)     
        
        if response['success'] == True:
            return sio.emit('category_response', {'data':"Category Updated Successfully", 'status': 'success', 'operation':'update_category'}, room=sid)
        else:
            return sio.emit('category_response', {'data':"Error updating Category", 'status': 'failure', 'operation':'update_category'}, room=sid)
    except Exception as e:
        # Handle other exceptions
        error_message = str(e)
        return sio.emit('category_response', {'data': error_message, 'status': 'failure', 'operation':'update_category'}, room=sid)


@sio.event
def cs_delete_category(sid, message):
    try:
        category_id = message['category_id']
        workspace_id = message['workspace_id']
        api_key = message['api_key']
        product = message['product']

        db_name = f"{workspace_id}_{product}"
        coll_name = f"{workspace_id}_category"

        response = data_cube.delete_data(api_key=api_key, db_name=db_name, coll_name=coll_name, query={"_id": category_id})

        if response['success']:
            if response['message']:
                return sio.emit('category_response', {'data': "Category Deleted Successfully", 'status': 'success', 'operation':'delete_category'}, room=sid)
            else:
                return sio.emit('category_response', {'data': 'No data found for this query', 'status': 'success', 'operation':'delete_category'}, room=sid)
        else:
            return sio.emit('category_response', {'data': response['message'], 'status': 'failure', 'operation':'delete_category'}, room=sid)

    except Exception as e:
        error_message = str(e)
        return sio.emit('category_response', {'data': error_message, 'status': 'failure', 'operation':'delete_category'}, room=sid)

@sio.event
def cs_add_category_member(sid, message):
    try:
        category_id = message['category_id']
        user_id = message['user_id']

        workspace_id = message['workspace_id']
        api_key = message['api_key']
        product = message['product']

        db_name = f"{workspace_id}_{product}"
        coll_name = f"{workspace_id}_category"

        is_category = data_cube.fetch_data(api_key=api_key, db_name=db_name, coll_name=coll_name, filters={"_id": category_id}, limit=1, offset=0)

        if not is_category['data']:
            return sio.emit('category_response', {'data': 'Category not found', 'status': 'failure', 'operation': 'add_category_member'}, room=sid)

        existing_member_list = is_category['data'][0].get('member_list', [])
        print(f"existing memember {existing_member_list}")
        # Check if user_id is already in the member_list
        if user_id in existing_member_list:
            return sio.emit('category_response', {'data': 'User is already a member', 'status': 'failure', 'operation': 'add_category_member'}, room=sid)

        # Add the user_id to the member_list
        updated_member_list = existing_member_list + [user_id]
        update_data = {
            "member_list": updated_member_list,
        }
        print(updated_member_list)

        response = data_cube.update_data(api_key=api_key,db_name=db_name, coll_name=coll_name, query={"_id": category_id}, update_data=update_data)

        if response['success']:
            return sio.emit('category_response', {'data': "User added Successfully", 'status': 'success', 'operation': 'add_category_member'}, room=sid)
        else:
            return sio.emit('category_response', {'data': "Error adding user", 'status': 'failure', 'operation': 'add_category_member'}, room=sid)

    except Exception as e:
        error_message = str(e)
        return sio.emit('category_response', {'data': error_message, 'status': 'failure', 'operation': 'add_category_member'}, room=sid)

@sio.event
def cs_delete_category_member(sid, message):
    try:
        category_id = message['category_id']
        user_id = message['user_id']

        workspace_id = message['workspace_id']
        api_key = message['api_key']
        product = message['product']

        db_name = f"{workspace_id}_{product}"
        coll_name = f"{workspace_id}_category"

        is_category = data_cube.fetch_data(api_key=api_key, db_name=db_name, coll_name=coll_name, filters={"_id": category_id}, limit=1, offset=0)

        if not is_category['data']:
            return sio.emit('category_response', {'data': 'Category not found', 'status': 'failure', 'operation': 'delete_category_member'}, room=sid)

        existing_member_list = is_category['data'][0].get('member_list', [])
        updated_member_list = [member for member in existing_member_list if member != user_id]

        update_data = {
            "member_list": updated_member_list,
        }

        response = data_cube.update_data(api_key=api_key, db_name=db_name, coll_name=coll_name, query={"_id": category_id}, update_data=update_data)

        if response['success']:
            return sio.emit('category_response', {'data': "User Removed Successfully", 'status': 'success', 'operation': 'delete_category_member'}, room=sid)
        else:
            return sio.emit('category_response', {'data': "Error removing user from Channel", 'status': 'failure', 'operation': 'delete_category_member'}, room=sid)

    except Exception as e:
        error_message = str(e)
        return sio.emit('category_response', {'data': error_message, 'status': 'failure', 'operation': 'delete_category_member'}, room=sid)


""" PUBLIC MESSAGE SECTION"""

@sio.event
def create_public_room(sid, message):
    try:
        name = message['public_link_id']
        category = message['category_id']
        created_at = message['created_at']
        linkid = message['linkid']
        workspace_id = message['workspace_id']
        api_key = message['api_key']
        product = message['product']

        db_name = f"{workspace_id}_{product}"
        coll_name = f"{workspace_id}_public_room"

        is_category = data_cube.fetch_data(api_key=api_key, db_name=db_name, coll_name=f"{workspace_id}_category", filters={"_id": category}, limit=1, offset=0)
        
        data = {
                "name": name,
                "category": category, 
                "display_name": None, 
                "is_active": True,
                "linkid": linkid,        
                "created_at": created_at, 
        }        

        if check_collection(workspace_id, "public_room"):
            check_collection(workspace_id, "public_chat")   

            is_room = data_cube.fetch_data(api_key=api_key, db_name=db_name, coll_name=coll_name, filters={"name": name}, limit=1, offset=0)

            if is_room['success']:
                if is_room['data']:

                    sio.enter_room(sid, is_room['data'][0]['_id'])

                    msg_response = data_cube.fetch_data(api_key=api_key,db_name=db_name, coll_name=f"{workspace_id}_public_chat", filters={"room_id": is_room['data'][0]['_id']}, limit=200, offset=0)
                    if msg_response['data']:
                        sio.emit('public_message_response', {'data': msg_response['data'], 'room_id':is_room['data'][0]['_id'], 'status': 'success', 'operation': 'create_public_room'}, room=sid)
                    else:
                        sio.emit('public_message_response', {'data': [], 'room_id':is_room['data'][0]['_id'], 'status': 'success', 'operation': 'create_public_room'}, room=sid)    
                    return


            response = data_cube.insert_data(api_key=api_key, db_name=db_name, coll_name=coll_name, data=data)

            if response['success'] == True:

                sio.enter_room(sid, response['data']['inserted_id'])
                sio.emit('public_message_response', {'data': "Hey,  Welcome to DoWell Customer Support. How may I assist you?", 'status': 'success', 'operation': 'create_public_room'}, room=name)

                new_room_date ={
                    '_id': response['data']['inserted_id'], 
                    'name': name, 
                    'category': category,
                    'server':is_category['data'][0]['server_id'],
                    'linkid': linkid
                    }

                sio.emit('new_public_room', {'data': new_room_date, 'status': 'success', }, room=category)
                
                existing_rooms = is_category['data'][0].get('rooms', [])
                updated_rooms = existing_rooms + [response['data']['inserted_id']]
                update_data = {
                    "rooms": updated_rooms,
                }

                response = data_cube.update_data(api_key=api_key,db_name=db_name, coll_name=f"{workspace_id}_category", query={"_id": category}, update_data=update_data)

                if response['success']:
                    return sio.emit('public_room_response', {'data': new_room_date, 'status': 'success', 'operation': 'create_public_room'}, room=sid)
                else:
                    return sio.emit('public_room_response', {'data': "Error Creating Room", 'status': 'failure', 'operation': 'create_public_room'}, room=sid)
            
            else:
                return sio.emit('public_room_response', {'data':"Error Creating Room", 'status': 'failure', 'operation':'create_public_room'}, room=sid)
    except Exception as e:
        # Handle other exceptions
        error_message = str(e)
        return sio.emit('public_room_response', {'data': error_message, 'status': 'failure', 'operation':'create_public_room'}, room=sid)

@sio.event
def public_join_room(sid, message):
    try:
        room = message['room_id']
        workspace_id = message['workspace_id']
        api_key = message['api_key']
        product = message['product']

        db_name = f"{workspace_id}_{product}"
        coll_name = f"{workspace_id}_public_room"
        response = data_cube.fetch_data(api_key=api_key,db_name=db_name, coll_name=coll_name, filters={"_id": room}, limit=1, offset=0)

        if response['success']:
            if not response['data']:
                return sio.emit('public_room_response', {'data': 'No Room found ', 'status': 'failure', 'operation':'join_public_room'}, room=sid)
            else:
                room_name = response['data'][0].get('_id', '')
                sio.enter_room(sid, room_name)
                msg_response = data_cube.fetch_data(api_key=api_key,db_name=db_name, coll_name=f"{workspace_id}_public_chat", filters={"room_id": room}, limit=200, offset=0)
                if msg_response['data']:
                    sio.emit('public_message_response', {'data': msg_response['data'], 'status': 'success', 'operation': 'join_public_room'}, room=sid)
                    
                    #Mark the messages as read
                    update_data = {
                        'is_read': True, 
                    }
                    mark_read = data_cube.update_data(api_key=my_api_key, db_name=db_name, coll_name=f"{workspace_id}_public_chat", query={"room_id": room}, update_data=update_data)
                    print(mark_read)
                else:
                    sio.emit('public_message_response', {'data': [], 'status': 'success', 'operation': 'join_public_room'}, room=sid)    
                return

    except Exception as e:
        # Handle other exceptions
        error_message = str(e)
        return sio.emit('public_message_response', {'data': error_message, 'status': 'failure', 'operation':'join_public_room'}, room=sid)


@sio.event
def public_message_event(sid, message):
    try:
        room_id = message['room_id']
        message_data = message['message_data']
        user_id = message['user_id']
        reply_to = message['reply_to']
        created_at = message['created_at']
        workspace_id = message['workspace_id']
        api_key = message['api_key']
        product = message['product']

        db_name = f"{workspace_id}_{product}"
        coll_name = f"{workspace_id}_public_chat"

        data = {
                    "room_id": room_id,
                    "message_data": message_data,
                    "author": user_id,
                    "reply_to": reply_to, 
                    "is_read": False,     
                    "created_at": created_at, 
        }

        sio.emit('public_message_response', {'data':data, 'status': 'success', 'operation':'send_message'}, room=room_id)

        response = data_cube.fetch_data(api_key=api_key,db_name=db_name, coll_name=f"{workspace_id}_public_room", filters={"_id": room_id}, limit=1, offset=0)
        if response['success']:
            if not response['data']:
                return sio.emit('public_room_response', {'data': 'No Room found ', 'status': 'failure', 'operation':'send_message'}, room=sid)
            else:
                room_name = response['data'][0].get('name', '')
                
                response = data_cube.insert_data(api_key=api_key,db_name=db_name, coll_name=coll_name, data=data)
                
                if response['success'] == True:
                    return 
                else:
                    return sio.emit('public_message_response', {'data':"Error sending message", 'status': 'failure', 'operation':'send_message'}, room=room_id)
    except Exception as e:
        error_message = str(e)
        return sio.emit('public_message_response', {'data': error_message, 'status': 'failure'}, room=room_id)



@sio.event
def auto_join_room(sid, message):
    try:
        user_id = message['user_id']
        workspace_id = message['workspace_id']
        api_key = message['api_key']
        product = message['product']

        db_name = f"{workspace_id}_{product}"
        coll_name_server = f"{workspace_id}_server"
        coll_name_category = f"{workspace_id}_category"
        coll_name_public_chat = f"{workspace_id}_public_chat"


        if product == "customer_support":
            response_servers = data_cube.fetch_data(
                api_key=api_key,
                db_name=db_name,
                coll_name=coll_name_server,
                filters={},
                limit=29,
                offset=0
            )
        else:
            response_servers = data_cube.fetch_data(
                api_key=api_key,
                db_name=db_name,
                coll_name=coll_name_server,
                filters={"$or": [{"owner": user_id}, {"member_list": {"$in": [user_id]}}]},
                limit=199,
                offset=0
            )

        result_data = []  

        if response_servers['success'] and response_servers['data']:
            for server in response_servers['data']:
                server_data = {"server_id": server["_id"], "category": []}

                # Get the categories in the server
                response_category = data_cube.fetch_data(
                    api_key=api_key,
                    db_name=db_name,
                    coll_name=coll_name_category,
                    filters={"server_id": str(server_data["server_id"])},
                    limit=199,
                    offset=0  
                )

                if response_category['success'] and response_category['data']:
                    for category in response_category['data']:
                        category_data = {"_id": category["_id"], "rooms": []}

                        # Get the rooms in the category
                        for room_id in category.get('rooms', []):
                            sio.enter_room(sid, str(room_id))

                            # Retrieve unread message count for the room
                            unread_messages = data_cube.fetch_data(
                                api_key=api_key,
                                db_name=db_name,
                                coll_name=coll_name_public_chat,
                                filters={"room_id": str(room_id), "is_read": False},
                                limit=1000,
                                offset=0
                            )

                            unread_message_count = len(unread_messages.get('data', []))

                            room_data = {
                                "_id": {"$oid": room_id},
                                "unread_message": unread_message_count,
                            }

                            category_data["rooms"].append(room_data)

                        server_data["category"].append(category_data)

                    result_data.append(server_data)


            return sio.emit('auto_join_response', {'data': result_data, 'status': 'success',
                                                   'operation': 'auto_join_room'}, room=sid)

        else:

            return sio.emit('auto_join_response', {'data': 'No servers found for the user', 'status': 'failure',
                                                   'operation': 'auto_join_room'}, room=sid)

    except Exception as e:
        error_message = str(e)
        return sio.emit('auto_join_response', {'data': error_message, 'status': 'failure',
                                               'operation': 'auto_join_room'}, room=sid)



@sio.event
def public_request_call(sid, message):
    try:
        room_id = message['room_id']
        sio.emit('public_room_response', {'data': f"{sid} Is Requesting for a Call",  'sid': f"{sid}", 'status': 'success',
                                               'operation': 'public_request_call'}, room=room_id, skip_sid=sid)
    except Exception as e:
        error_message = str(e)
        return sio.emit('public_room_response', {'data': error_message, 'status': 'failure',
                                               'operation': 'public_request_call'}, room=sid)

@sio.event
def set_public_room_display_name(sid, message):
    try:

        room_id = message['room_id']
        display_name = message['display_name']
        

        workspace_id = message['workspace_id']
        api_key = message['api_key']
        product = message['product']

        db_name = f"{workspace_id}_{product}"
        coll_name = f"{workspace_id}_public_room"       


        update_data = {
                "display_name": display_name,
        }

        response = data_cube.update_data(api_key=api_key, db_name=db_name, coll_name=coll_name, query = {"_id": room_id}, update_data=update_data)     
        
        return_data = {
             "display_name": display_name,
             "_id": room_id
        }
        if response['success'] == True:
            return sio.emit('public_room_response', {'data':return_data, 'status': 'success', 'operation':'set_display_name'}, room=sid)
        else:
            return sio.emit('public_room_response', {'data':"Error setting display name", 'status': 'failure', 'operation':'set_display_name'}, room=sid)
    except Exception as e:
        # Handle other exceptions
        error_message = str(e)
        return sio.emit('public_room_response', {'data': error_message, 'status': 'failure', 'operation':'set_display_name'}, room=sid)



""" MASTER LINK EVENTS """
@sio.event
def get_used_usernames(sid, message):
    try:
        workspace_id = message['workspace_id']
        api_key = message['api_key']
        product = message['product']

        db_name = f"{workspace_id}_{product}"
        coll_name = f"{workspace_id}_master_link"

        check_collection(workspace_id, "master_link")
        response = data_cube.fetch_data(api_key=my_api_key,db_name=db_name, coll_name=coll_name, filters={"workspace_id": workspace_id}, limit=1, offset=0)
        if response['success']:
            return sio.emit('master_link_response', {'data': response['data'], 'status': 'success', 'operation': 'get_used_usernames'}, room=sid)

    except Exception as e:
        error_message = str(e)
        return sio.emit('master_link_response', {'data': error_message, 'status': 'failure', 'operation': 'get_used_usernames'}, room=sid)

@sio.event
def create_master_link(sid, message):
    try:
        company_id = message['workspace_id']
        links = message['links']
        job_name = message['job_name']
        url = "https://www.qrcodereviews.uxlivinglab.online/api/v3/qr-code/"

        db_name = f"{company_id}_{job_name}"
        coll_name = f"{company_id}_master_link"

        is_First = False
        

        check_collection(company_id, "master_link")
        coll_response = data_cube.fetch_data(api_key=my_api_key,db_name=db_name, coll_name=coll_name, filters={"workspace_id": company_id}, limit=1, offset=0)
        if coll_response['success']:
            if not coll_response['data']:
                is_First = True
            else:
                used_links = coll_response['data'][0]['public_username']
                new_links = get_link_usernames(links)



        payload = {
            "qrcode_type": "Link",
            "quantity": 1,
            "company_id": company_id,
            "links": links,
            "document_name": job_name,
        }

        response = requests.post(url, json=payload)

        if response.status_code == 201:
            sio.emit('master_link_response', {'data': json.loads(response.text), 'status': 'success', 'operation': 'create_master_link'}, room=sid)

            if is_First:
                data = {
                    "workspace_id": company_id,
                    "public_username": get_link_usernames(links),  # Corrected variable name
                }
                add_response = data_cube.insert_data(api_key=my_api_key, db_name=db_name, coll_name=coll_name, data=data)
                print(add_response)
            else:
                update_data = {
                    "workspace_id": company_id,
                    "public_username": used_links + new_links,
                }

                add_response = data_cube.update_data(api_key=my_api_key, db_name=db_name, coll_name=coll_name, query={"workspace_id": company_id}, update_data=update_data)
                print(add_response)

            return
        else:
            # Error response
            return sio.emit('master_link_response', {'data': f"Error: {json.loads(response.text)}", 'status': 'failure', 'operation': 'create_master_link'}, room=sid)

    except Exception as e:
        error_message = str(e)
        return sio.emit('master_link_response', {'data': error_message, 'status': 'failure', 'operation': 'create_master_link'}, room=sid)

@sio.event
def set_finalize(sid, message):
    try:
        linkid = message['linkid']
        room_id = message['room_id']
        workspace_id = message['workspace_id']
        api_key = message['api_key']
        product = message['product']

        db_name = f"{workspace_id}_{product}"
        coll_name = f"{workspace_id}_public_room"

        
        url = f"https://www.qrcodereviews.uxlivinglab.online/api/v3/masterlink/?link_id={linkid}"
        payload = {
            "is_finalized": True,
        }
        response = requests.put(url, json=payload)

        if response.status_code == 200:
            update_data = {
                    "is_active": False
            }

            room_response = data_cube.update_data(api_key=api_key, db_name=db_name, coll_name=coll_name, query = {"_id": room_id}, update_data=update_data)     
            
            if room_response['success'] == True:
                sio.emit('master_link_response', {'data':"Room Set as Inactive", 'status': 'success', 'operation':'set_finalize'}, room=sid)
            else:
                return sio.emit('master_link_response', {'data':"Error updating Room", 'status': 'failure', 'operation':'set_finalize'}, room=sid)

            
            return sio.emit('master_link_response', {'data': json.loads(response.text), 'status': 'success', 'operation': 'set_finalize'}, room=sid)
        else:
            # Error response
            return sio.emit('master_link_response', {'data': f"Error: {json.loads(response.text)}", 'status': 'failure', 'operation': 'set_finalize'}, room=sid)

    except Exception as e:
        error_message = str(e)
        return sio.emit('master_link_response', {'data': error_message, 'status': 'failure', 'operation': 'set_finalize'}, room=sid)


@sio.event
def remove_public_usernames(sid, message):
    try:
        org_id = message['workspace_id']
        product = message['product']
        usernames = message['usernames']
        
        payload = {
        "org_id":org_id,
        "product":product,
        "usernames": usernames
        }
        url = "https://100093.pythonanywhere.com/api/remove_public_usernames/"
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            # Successful response
            return sio.emit('master_link_response', {'data': json.loads(response.text), 'status': 'success', 'operation': 'remove_public_usernames'}, room=sid)
        else:
            # Error response
            return sio.emit('master_link_response', {'data': f"Error: {json.loads(response.text)}", 'status': 'failure', 'operation': 'remove_public_usernames'}, room=sid)

    except Exception as e:
        error_message = str(e)
        return sio.emit('master_link_response', {'data': error_message, 'status': 'failure', 'operation': 'remove_public_usernames'}, room=sid)



"""NOTIFICATION EVENTS"""
@sio.event
def get_user_rooms(sid):
    rooms = sio.rooms(sid)
    return sio.emit('user_rooms_response', {'rooms': list(rooms)}, room=sid)

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



""" 
=============================================================================================

                CUSTOMER SUPPORT VERSION 2 STARTS HERE

===============================================================================================
"""
 
##TODO - Create DB 0 
##TODO - Create an event for adding topics and also for retrieving topics
##TODO - Create another event for other settings in the DB 0
##NOTE: While creating a topic: check if the DB for that topic exists

"""TOPIC RELATED EVENTS"""
@sio.event
def create_topic(sid, message):
    try:
        workspace_id = message['workspace_id']
        api_key = message['api_key']

        name = message ['name'].upper().replace(" ", "_")
        created_at = message['created_at']
        
        data = {
                "name": name,
                "created_at": created_at, 
        }
        
        db_name = f"{workspace_id}_CUSTOMER_SUPPORT_DB0"
        coll_name = "topics"
        topic_db = f"{workspace_id}_{name}"

        

        #Check if the DB0 Exists
        if not check_db(workspace_id, db_name):
            return sio.emit('setting_response', {'data':f"DB {db_name} Not found", 'status': 'failure', 'operation':'create_topic'}, room=sid)

        #Check if the DB for the topic exists
        if not check_db(workspace_id, topic_db):
            return sio.emit('setting_response', {'data':f"DB {workspace_id}_{name.upper()} Not found", 'status': 'failure', 'operation':'create_topic'}, room=sid)    

        
        if check_collection(workspace_id, "topics", db_name):
            
            check_topic = data_cube.fetch_data(api_key=api_key,db_name=db_name, coll_name=coll_name, filters={"name":name},limit=200, offset=0)
            if check_topic['success']:
                if check_topic['data']:
                    return sio.emit('setting_response', {'data':f"Topic {name} already exists", 'status': 'failure', 'operation':'create_topic'}, room=sid)

            response = data_cube.insert_data(api_key=api_key, db_name=db_name, coll_name=coll_name, data=data)

            if response['success'] == True:
                return sio.emit('setting_response', {'data':response['data'], 'status': 'success', 'operation':'create_topic'}, room=sid)
            else:
                return sio.emit('setting_response', {'data':response['message'], 'status': 'failure', 'operation':'create_topic'}, room=sid)
    except Exception as e:
        # Handle other exceptions
        error_message = str(e)
        return sio.emit('setting_response', {'data': error_message, 'status': 'failure', 'operation':'create_topic'}, room=sid)


@sio.event
def get_all_topics(sid, message):
    try:
        workspace_id = message['workspace_id']
        api_key = message['api_key']
        

        db_name = f"{workspace_id}_CUSTOMER_SUPPORT_DB0"
        coll_name = "topics"

        if not check_db(workspace_id, db_name):
            return sio.emit('setting_response', {'data':f"DB {db_name} Not found", 'status': 'failure', 'operation':'get_all_topics'}, room=sid)

        if check_collection(workspace_id, "topics", db_name):

            response = data_cube.fetch_data(
                api_key=api_key,
                db_name=db_name,
                coll_name=coll_name,
                filters={},
                limit=199,
                offset=0
            )
        
            if response['success']:
                sio.enter_room(sid, workspace_id)
                if not response['data']:
                    return sio.emit('setting_response', {'data': 'No Topic found for this Workspace', 'status': 'failure', 'operation': 'get_all_topics'}, room=sid)

                else:
                    return sio.emit('setting_response', {'data': response['data'], 'status': 'success', 'operation': 'get_all_topics'}, room=sid)
            else:
                # Error in fetching data
                return sio.emit('setting_response', {'data': response['message'], 'status': 'failure', 'operation': 'get_all_topics'}, room=sid)

    except Exception as e:
        # Handle other exceptions
        error_message = str(e)
        return sio.emit('setting_response', {'data': error_message, 'status': 'failure', 'operation': 'get_all_topics'}, room=sid)


""" LINE MANAGER RELATED EVENTS"""
@sio.event
def create_line_manager(sid, message):
    try:
        user_id = message['user_id']
        created_at = message['created_at']
        workspace_id = message['workspace_id']
        api_key = message['api_key']

        
        
        data = {
                "user_id": user_id,
                "positions_in_a_line": calculate_position_in_line(api_key, workspace_id),
                "average_serving_time":0,
                "ticket_count": 0,
                "is_active": True,
                "created_at": created_at, 
        }
        
        db_name = f"{workspace_id}_CUSTOMER_SUPPORT_DB0"
        coll_name = "line_manager"

        

        #Check if the DB0 Exists
        if not check_db(workspace_id, db_name):
            return sio.emit('setting_response', {'data':f"DB {db_name} Not found", 'status': 'failure', 'operation':'create_line_manager'}, room=sid)

       
        
        if check_collection(workspace_id, "line_manager", db_name):
            
            check_user = data_cube.fetch_data(api_key=api_key,db_name=db_name, coll_name=coll_name, filters={"user_id":user_id},limit=200, offset=0)
            if check_user['success']:
                if check_user['data']:
                    return sio.emit('setting_response', {'data':f"User {user_id} already exists", 'status': 'failure', 'operation':'create_line_manager'}, room=sid)

            response = data_cube.insert_data(api_key=api_key, db_name=db_name, coll_name=coll_name, data=data)

            if response['success'] == True:
                return sio.emit('setting_response', {'data':response['data'], 'status': 'success', 'operation':'create_line_manager'}, room=sid)
            else:
                return sio.emit('setting_response', {'data':response['message'], 'status': 'failure', 'operation':'create_line_manager'}, room=sid)
    except Exception as e:
        # Handle other exceptions
        error_message = str(e)
        return sio.emit('setting_response', {'data': error_message, 'status': 'failure', 'operation':'create_line_manager'}, room=sid)


@sio.event
def get_all_line_managers(sid, message):
    try:
        workspace_id = message['workspace_id']
        api_key = message['api_key']
        

        db_name = f"{workspace_id}_CUSTOMER_SUPPORT_DB0"
        coll_name = "line_manager"

        if not check_db(workspace_id, db_name):
            return sio.emit('setting_response', {'data':f"DB {db_name} Not found", 'status': 'failure', 'operation':'get_all_line_managers'}, room=sid)

        if check_collection(workspace_id, "line_manager", db_name):

            response = data_cube.fetch_data(
                api_key=api_key,
                db_name=db_name,
                coll_name=coll_name,
                filters={},
                limit=199,
                offset=0
            )
        
            if response['success']:
                if not response['data']:
                    return sio.emit('setting_response', {'data': 'No Line Manager found for this Workspace', 'status': 'failure', 'operation': 'get_all_line_managers'}, room=sid)

                else:
                    return sio.emit('setting_response', {'data': response['data'], 'status': 'success', 'operation': 'get_all_line_managers'}, room=sid)
            else:
                # Error in fetching data
                return sio.emit('setting_response', {'data': response['message'], 'status': 'failure', 'operation': 'get_all_line_managers'}, room=sid)

    except Exception as e:
        # Handle other exceptions
        error_message = str(e)
        return sio.emit('setting_response', {'data': error_message, 'status': 'failure', 'operation': 'get_all_line_managers'}, room=sid)


@sio.event
def merge_line(sid, message):
    try:
        line_manager_1 = message['line_manager_1']
        line_manager_2 = message['line_manager_2']
        product = message['product']
        workspace_id = message['workspace_id']
        api_key = message['api_key']
        
        db_name = f"{workspace_id}_CUSTOMER_SUPPORT_DB0"
        coll_name = "line_manager"

        line_manager_1_response = data_cube.fetch_data(
            api_key=api_key,
            db_name=db_name,
            coll_name=coll_name,
            filters={'user_id': line_manager_1},
            limit=1,
            offset=0
        )
        
        line_manager_2_response = data_cube.fetch_data(
            api_key=api_key,
            db_name=db_name,
            coll_name=coll_name,
            filters={'user_id': line_manager_2},
            limit=1,
            offset=0
        )

        if line_manager_1_response['success'] and line_manager_2_response['success']:
            if not line_manager_1_response['success'] and line_manager_2_response['success']:
                return sio.emit('setting_response', {'data': 'Line Manager Not found ', 'status': 'failure', 'operation': 'merge_line'}, room=sid)
            
            product_db = f"{workspace_id}_{product}"
            collections = get_database_collections(api_key, product_db)

            total_tickets_updated = 0
            for coll_name in collections:
                response = data_cube.update_data(
                    api_key=api_key,
                    db_name=product_db,
                    coll_name=coll_name,
                    query={'line_manager': line_manager_1},
                    update_data={'line_manager': line_manager_2}
                )
                print(response)
                if response['success'] and response['message'] != '0 documents updated successfully!':
                    match = re.search(r'(\d+) documents updated successfully', response['message'])
                    if match:
                        total_tickets_updated += int(match.group(1))


            if total_tickets_updated > 0:
                # Update line manager's ticket count
                line_manage_1_ticket_count = line_manager_1_response['data'][0]['ticket_count'] - total_tickets_updated
                line_manage_2_ticket_count = line_manager_2_response['data'][0]['ticket_count'] + total_tickets_updated

                if line_manage_1_ticket_count  < 1:
                    line_manage_1_ticket_count = 0
                
                update_line_manager_1_response = data_cube.update_data(
                    api_key=api_key,
                    db_name=db_name,
                    coll_name="line_manager",
                    query={'user_id': line_manager_1},
                    update_data={"ticket_count": line_manage_1_ticket_count, "is_active": False}
                )

                update_line_manager_2_response = data_cube.update_data(
                    api_key=api_key,
                    db_name=db_name,
                    coll_name="line_manager",
                    query={'user_id': line_manager_2},
                    update_data={"ticket_count": line_manage_2_ticket_count}
                )



                if update_line_manager_1_response['success'] and update_line_manager_2_response['success']:
                    print(f"Ticket count updated for line managers")
                else:
                    print("Failed to update ticket count for line managers")
                
                sio.emit('setting_response', {'data': "Line Merged Successfully", 'status': 'success', 'operation': 'merge_line'}, room=sid)
            else:
                sio.emit('setting_response', {'data': "No Tickets Updated or Line Already Merged", 'status': 'failure', 'operation': 'merge_line'}, room=sid)
            
            return

    except Exception as e:
        # Handle other exceptions
        error_message = str(e)
        return sio.emit('setting_response', {'data': error_message, 'status': 'failure', 'operation': 'merge_line'}, room=sid)


# @sio.event
# def create_meta_settings(sid, message):
#     try:
#         workspace_id = message['workspace_id']
#         api_key = message['api_key']
#         product = message['product']

#         topics = message ['topics']
#         waiting_time = message['waiting_time']
#         operation_time = message['operation_time']
#         line_manager = message['line_manager']
#         created_at = message['created_at']
        
#         data = {
#                 "topics": topics,
#                 "waiting_time": waiting_time,
#                 "operation_time": operation_time,
#                 "line_manager": line_manager,
#                 "workspace_id":workspace_id,
#                 "created_at": created_at, 
#         }
        
#         db_name = f"{workspace_id}_{product}"
#         coll_name = f"{workspace_id}_CUSTOMER_SUPPORT_DB0"

#         if not check_db(workspace_id):
#             return sio.emit('setting_response', {'data':"No DB found for the Workspace", 'status': 'failure', 'operation':'create_meta_settings'}, room=sid)
#         if check_collection(workspace_id, "server"):
#             response = data_cube.insert_data(api_key=api_key, db_name=db_name, coll_name=coll_name, data=data)

#             if response['success'] == True:
#                 return sio.emit('setting_response', {'data':response['data'], 'status': 'success', 'operation':'create_meta_settings'}, room=sid)
#             else:
#                 return sio.emit('setting_response', {'data':response['message'], 'status': 'failure', 'operation':'create_meta_settings'}, room=sid)
#     except Exception as e:
#         # Handle other exceptions
#         error_message = str(e)
#         return sio.emit('setting_response', {'data': error_message, 'status': 'failure', 'operation':'create_meta_settings'}, room=sid)

""" TICKET CHAT STARTS HERE"""
@sio.event
def ticket_message_event(sid, message):
    producerTicketChat = ProducerTicketChat()
    try:

        ticket_id = message['ticket_id']
        message_data = message['message_data']
        user_id = message['user_id']
        reply_to = message['reply_to']
        created_at = message['created_at']
        workspace_id = message['workspace_id']
        api_key = message['api_key']
        product = message['product']

        data = {
                    "document_type": "chat",
                    "ticket_id": ticket_id,
                    "message_data": message_data,
                    "author": user_id,
                    "reply_to": reply_to, 
                    "is_read": False,     
                    "created_at": created_at, 
                    "product": product.upper(),
                    "workspace_id":workspace_id,
                    "api_key": api_key,
                    "sid":sid

        }

        sio.enter_room(sid, ticket_id)
        sio.emit('ticket_message_response', {'data':data, 'status': 'success', 'operation':'send_message'}, room=ticket_id)
        producerTicketChat.publish(data)

    except Exception as e:
        error_message = str(e)
        return sio.emit('ticket_message_response', {'data': error_message, 'status': 'failure'}, room=sid)

@sio.event
def get_ticket_messages(sid, message):
    try:
        ticket = message['ticket_id']
        workspace_id = message['workspace_id']
        api_key = message['api_key']
        product = message['product']

        db_name = f"{workspace_id}_{product.upper()}"
        coll_name = "2024_02_26_collection"
        response = data_cube.fetch_data(api_key=api_key,db_name=db_name, coll_name=coll_name, filters={"document_type":"ticket", "_id":ticket}, limit=1, offset=0)

        if response['success']:
            if response['data']:
                return sio.emit('ticket_message_response', {'data': 'No Ticket found ', 'status': 'failure', 'operation':'get_ticket_messages'}, room=sid)
            else:
                sio.enter_room(sid, ticket)
                collections = get_database_collections(api_key, db_name)
               
                message_filters = {"document_type": "chat", "ticket_id": ticket}
                messages = fetch_data_from_collections(api_key, db_name, collections, message_filters)

                
                # msg_response = data_cube.fetch_data(api_key=api_key,db_name=db_name, coll_name=coll_name, filters={"document_type":"chat", "ticket_id":ticket}, limit=50, offset=0)
                if messages:
                    sio.emit('ticket_message_response', {'data': messages, 'status': 'success', 'operation': 'get_ticket_messages'}, room=sid)
                    
                    #Mark the messages as read
                    update_data = {
                        'is_read': True, 
                    }
                    for coll_name in collections:
                        mark_read = data_cube.update_data(api_key=my_api_key, db_name=db_name, coll_name=coll_name, query={"document_type":"ticket", "ticket_id":ticket}, update_data=update_data)
                    
                else:
                    sio.emit('ticket_message_response', {'data': [], 'status': 'success', 'operation': 'get_ticket_messages'}, room=sid)    
                return

    except Exception as e:
        # Handle other exceptions
        error_message = str(e)
        return sio.emit('ticket_message_response', {'data': error_message, 'status': 'failure', 'operation':'get_ticket_messages'}, room=sid)


@sio.event
def create_ticket(sid, message):
    try:

        email = message['email']
        created_at = message['created_at']
        link_id = message['link_id']
        workspace_id = message['workspace_id']
        api_key = message['api_key']
        product = message['product'].upper()
        
        line_manager = assign_ticket_to_line_manager(api_key, f"{workspace_id}_CUSTOMER_SUPPORT_DB0", "line_manager", {})
        
        link_db_name = f"{workspace_id}_CUSTOMER_SUPPORT_DB0"
        link_coll_name = "master_link"
        
        link_response = data_cube.fetch_data(api_key=api_key, db_name=link_db_name, coll_name=link_coll_name,
            filters={"link_id":link_id},
            limit=1,
            offset=0
        )

        if link_response['success']:
            if link_response['data']:
               usernames = link_response['data'][0]['usernames']
               if usernames:
                   user_id = random.choice(usernames) if usernames else usernames[0]
               else:
                   return sio.emit('ticket_response', {'data':"Can't create Room due to no public username in the link_id", 'status': 'failure', 'operation':'create_ticket'}, room=sid)
                   

        
        
        data = {
                    "document_type": "ticket",
                    "user_id": user_id,
                    "email": email,
                    "display_name": None,
                    "line_manager": line_manager, 
                    "is_closed": False,     
                    "created_at": created_at, 
                    "updated_at": created_at,
                    "product": product.upper(),

        }

        formatted_date = str(date.today()).replace("-", "_")
        db_name = f"{workspace_id}_{product}"
        coll_name = f"{formatted_date}_collection"

        if check_daily_collection(workspace_id, product):
                            
            response = data_cube.insert_data(api_key=api_key,db_name=db_name, coll_name=coll_name, data=data)
            
            if response['success'] == True:
                sio.enter_room(sid, response['data']['inserted_id'])
        
                new_ticket_data ={
                    '_id': response['data']['inserted_id'], 
                    "user_id": user_id,
                    "display_name": None,
                    "line_manager": line_manager, 
                    "is_closed": False,     
                    "created_at": created_at, 
                    "updated_at": created_at,
                    "product": product,
                    }

                sio.emit('new_ticket', {'data': new_ticket_data, 'status': 'success', }, room=workspace_id)
                
                sio.emit('ticket_response', {'data': new_ticket_data, 'status': 'success', 'operation': 'create_ticket'}, room=sid)

                #Update the Master Link
                new_available_link = link_response['data'][0]['available_links'] 
                new_available_link -=1

                is_active = True
                if new_available_link == 0:
                    is_active = False

                usernames.remove(str(user_id))

                new_product = link_response['data'][0]['product_distribution'].copy() 
                new_product[product.upper()] -= 1


                update_link_response = data_cube.update_data(
                        api_key=api_key,
                        db_name=link_db_name, 
                        coll_name=link_coll_name,
                        query={'link_id': link_id},
                        update_data={
                            "available_links": new_available_link,
                            "product_distribution": new_product,
                            "usernames": usernames,
                            "is_active": is_active,
                        }
                    )

                """SENDING OF EMAIL"""

                formatted_email = EMAIL_FROM_WEBSITE.format(response['data']['inserted_id'], response['data']['inserted_id'])
                if is_valid_email(email):
                    send_email(email, email, "New Ticket Confirmation", formatted_email)
                else:
                    print("Email is invalid")


                return
                
            else:
                return sio.emit('ticket_response', {'data':"Error Creating Room", 'status': 'failure', 'operation':'create_ticket'}, room=sid)
    except Exception as e:
        # Handle other exceptions
        error_message = str(e)
        return sio.emit('ticket_response', {'data': error_message, 'status': 'failure', 'operation':'create_ticket'}, room=sid)


@sio.event
def get_tickets(sid, message):
    try:
        # user_id = message['user_id']
        workspace_id = message['workspace_id']
        api_key = message['api_key']
        product = message['product']

        db_name = f"{workspace_id}_{product.upper()}"
        
        collections = get_database_collections(api_key, db_name)
        
        ticket_filters = {"document_type": "ticket"}
        tickets = fetch_data_from_collections(api_key, db_name, collections, ticket_filters)

       
        if tickets:
            sio.emit('ticket_response', {'data': tickets, 'status': 'success', 'operation': 'get_ticket'}, room=sid)
             
        else:
            sio.emit('ticket_response', {'data': [], 'status': 'success', 'operation': 'get_ticket'}, room=sid)    
        return

    except Exception as e:
        # Handle other exceptions
        error_message = str(e)
        return sio.emit('ticket_response', {'data': error_message, 'status': 'failure', 'operation':'get_ticket'}, room=sid)

@sio.event
def close_ticket(sid, message):
    try:
        ticket_id = message['ticket_id']
        line_manager = message['line_manager']
        workspace_id = message['workspace_id']
        api_key = message['api_key']
        product = message['product']

        db_name = f"{workspace_id}_{product.upper()}"
        
        collections = get_database_collections(api_key, db_name)

        ticket_closed = False
        for coll_name in collections:
            response = data_cube.update_data(
                api_key=api_key,
                db_name=db_name,
                coll_name=coll_name,
                query={'_id': ticket_id},
                update_data={'is_closed': True}
            )
            if response['success'] and response['message'] != '0 documents updated successfully!':
                ticket_closed = True
                sio.emit('ticket_response', {'data': "Ticket Closed", 'status': 'success', 'operation': 'close_ticket'}, room=sid)
                
                # Update line manager's ticket count
                line_manager_db_name = f"{workspace_id}_CUSTOMER_SUPPORT_DB0"
                line_manager_coll_name = "line_manager"
                line_manager_data = data_cube.fetch_data(
                    api_key=api_key,
                    db_name=line_manager_db_name,
                    coll_name=line_manager_coll_name,
                    filters={'user_id': line_manager},
                    limit=1,
                    offset=0
                )

                if line_manager_data:
                    new_ticket_count = line_manager_data['data'][0]['ticket_count'] 
                    new_ticket_count -=1
                    line_manager_response = data_cube.update_data(
                        api_key=api_key,
                        db_name=line_manager_db_name,
                        coll_name=line_manager_coll_name,
                        query={'user_id': line_manager},
                        update_data={"ticket_count":new_ticket_count}
                    )


                    if line_manager_response['success']:
                        print(f"Ticket count updated for line manager: {line_manager}")
                    else:
                        print("Failed to update ticket count for line manager:", line_manager_response['message'])
                else:
                    print("Line manager not found:", line_manager)


                break

        if not ticket_closed:
            sio.emit('ticket_response', {'data': "Ticket Already Closed", 'status': 'success', 'operation': 'close_ticket'}, room=sid)    

        return

    except Exception as e:
        # Handle other exceptions
        error_message = str(e)
        return sio.emit('ticket_response', {'data': error_message, 'status': 'failure', 'operation':'close_ticket'}, room=sid)

@sio.event
def reopen_ticket(sid, message):
    try:
        ticket_id = message['ticket_id']
        line_manager = message['line_manager']
        workspace_id = message['workspace_id']
        api_key = message['api_key']
        product = message['product']

        db_name = f"{workspace_id}_{product.upper()}"
        
        collections = get_database_collections(api_key, db_name)

        ticket_closed = False
        for coll_name in collections:
            response = data_cube.update_data(
                api_key=api_key,
                db_name=db_name,
                coll_name=coll_name,
                query={'_id': ticket_id},
                update_data={'is_closed': False}
            )
            if response['success'] and response['message'] != '0 documents updated successfully!':
                ticket_closed = True
                sio.emit('ticket_response', {'data': "Ticket Reopened", 'status': 'success', 'operation': 'reopen_ticket'}, room=sid)
                
                # Update line manager's ticket count
                line_manager_db_name = f"{workspace_id}_CUSTOMER_SUPPORT_DB0"
                line_manager_coll_name = "line_manager"
                line_manager_data = data_cube.fetch_data(
                    api_key=api_key,
                    db_name=line_manager_db_name,
                    coll_name=line_manager_coll_name,
                    filters={'user_id': line_manager},
                    limit=1,
                    offset=0
                )

                if line_manager_data:
                    new_ticket_count = line_manager_data['data'][0]['ticket_count'] 
                    new_ticket_count +=1
                    line_manager_response = data_cube.update_data(
                        api_key=api_key,
                        db_name=line_manager_db_name,
                        coll_name=line_manager_coll_name,
                        query={'user_id': line_manager},
                        update_data={"ticket_count":new_ticket_count}
                    )


                    if line_manager_response['success']:
                        print(f"Ticket count updated for line manager: {line_manager}")
                    else:
                        print("Failed to update ticket count for line manager:", line_manager_response['message'])
                else:
                    print("Line manager not found:", line_manager)


                break

        if not ticket_closed:
            sio.emit('ticket_response', {'data': "Ticket Already Reopened", 'status': 'success', 'operation': 'reopen_ticket'}, room=sid)    

        return

    except Exception as e:
        # Handle other exceptions
        error_message = str(e)
        return sio.emit('ticket_response', {'data': error_message, 'status': 'failure', 'operation':'reopen_ticket'}, room=sid)


""" SHARE LINK SECTION"""
@sio.event
def generate_share_link(sid, message):
    try:
        number_of_links = message['number_of_links']
        product_distribution = message['product_distribution']
        usernames = message['usernames']
        url = message['url']
        created_at = message['created_at']
        workspace_id = message['workspace_id']
        api_key = message['api_key']

        link_id = ''.join([str(random.randint(0, 9)) for _ in range(20)])
        link = f"{url}?workspace_id={workspace_id}&link_id={link_id}"
        # master_link = f"http://127.0.0.1:8000/share/?link_id={link_id}&workspace_id={workspace_id}&link_key={api_key}"
        master_link = f"https://www.dowellchat.uxlivinglab.online/api/share/?link_id={link_id}&workspace_id={workspace_id}&link_key={api_key}"

        data = {
            "link_id":link_id,
            "number_of_links": number_of_links,
            "available_links": number_of_links,
            "product_distribution": product_distribution,
            "link": link,
            "usernames": usernames,
            "is_active": True,
            "master_link": master_link,
            "created_at": created_at
        }


        db_name = f"{workspace_id}_CUSTOMER_SUPPORT_DB0"
        coll_name = "master_link"
  
        #Check if the DB0 Exists
        if not check_db(workspace_id, db_name):
            return sio.emit('share_link_response', {'data':f"DB {db_name} Not found", 'status': 'failure', 'operation':'generate_share_link'}, room=sid)

        if check_collection(workspace_id, "master_link", db_name):            
            response = data_cube.insert_data(api_key=api_key, db_name=db_name, coll_name=coll_name, data=data)

            if response['success'] == True:
                return sio.emit('share_link_response', {'data':master_link, 'status': 'success', 'operation':'generate_share_link'}, room=sid)
            else:
                return sio.emit('share_link_response', {'data':response['message'], 'status': 'failure', 'operation':'generate_share_link'}, room=sid)
    except Exception as e:
        # Handle other exceptions
        error_message = str(e)
        return sio.emit('share_link_response', {'data': error_message, 'status': 'failure', 'operation':'generate_share_link'}, room=sid)



def redirect_to_product_link(request):
    try:
        link_id = request.GET['link_id']
        workspace_id = request.GET['workspace_id']
        api_key = request.GET['link_key']

        db_name = f"{workspace_id}_CUSTOMER_SUPPORT_DB0"
        coll_name = "master_link"
        filters = {"link_id": link_id, "is_active": True, "available_links": { "$ne": 0 }}

        find_link = data_cube.fetch_data(api_key=api_key,db_name=db_name, coll_name=coll_name, filters=filters,limit=1, offset=0)
        print(find_link)
        if find_link['success']:
            if find_link['data']:
                redirect_url = find_link['data'][0]['link']
                return redirect(redirect_url)
            
        
        return render(request, 'api/error.html')
    except KeyError as e:
        context = {
            "error": e
        }
        
        return render(request, 'api/error.html', context)
        # return HttpResponse(f"Missing parameter: {e}")
    
@sio.event
def get_share_link_details(sid, message):
    try:
        link_id = message['link_id']
        workspace_id = message['workspace_id']
        api_key = message['api_key']

        db_name = f"{workspace_id}_CUSTOMER_SUPPORT_DB0"
        coll_name = "master_link"

        
        
        response = data_cube.fetch_data(
            api_key=api_key,
            db_name=db_name,
            coll_name=coll_name,
            filters={"link_id":link_id},
            limit=1,
            offset=0
        )
    
        if response['success']:
            if not response['data']:
                return sio.emit('share_link_response', {'data': 'Link not found', 'status': 'failure', 'operation': 'get_share_link_details'}, room=sid)

            else:
                return sio.emit('share_link_response', {'data': response['data'], 'status': 'success', 'operation': 'get_share_link_details'}, room=sid)
        else:
            # Error in fetching data
            return sio.emit('share_link_response', {'data': response['message'], 'status': 'failure', 'operation': 'get_share_link_details'}, room=sid)
        
        
    except Exception as e:
        # Handle other exceptions
        error_message = str(e)
        return sio.emit('share_link_response', {'data': error_message, 'status': 'failure', 'operation':'get_share_link_details'}, room=sid)
