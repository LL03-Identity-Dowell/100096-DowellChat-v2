import json
import os
import sys 
import threading
from confluent_kafka import Consumer
from confluent_kafka import KafkaError
from confluent_kafka import KafkaException
from datetime import date
from .utils import (
    processApiService, 
    DataCubeConnection, 
    create_cs_db_meta, 
    check_db, 
    check_collection, 
    get_link_usernames,
    get_room_details, 
    get_safe_timestamp,
    sanitize_filename,
    check_daily_collection
    )
from .views import sio

#We want to run thread in an infinite loop
running=True
kafka_environ = os.getenv("ENVIRON")
conf = {'bootstrap.servers': f"{kafka_environ}:9092",
        'auto.offset.reset': 'smallest',
        'group.id': "user_group"}
#Topic
topic='ticket_chat_topic_test'

data_cube = DataCubeConnection()


class ChatCreatedListener(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # Create consumer
        self.consumer = Consumer(conf)
   
        
    def run(self):
        print ('Created Listener ')
        try:
            #Subcribe to topic
            self.consumer.subscribe([topic])
            while running:
                #Poll for message
                msg = self.consumer.poll(timeout=1.0)
                if msg is None: continue
                #Handle Error
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                        sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
                else:
                    #Handle Message
                    print('---------> Got message Sending to MongoDB.....')
                    message = json.loads(msg.value().decode('utf-8'))
                    
                    workspace_id = message['workspace_id']
                    product = message['product']
                    api_key = message['api_key']
                    sid = message['sid']

                    print(message)

                    #Removing of some keys
                    unwanted_keys=['workspace_id', 'product', 'api_key', 'sid']

                    for key in unwanted_keys:
                        message.pop(key, None)
                    

                    formatted_date = str(date.today()).replace("-", "_")
                    db_name = f"{workspace_id}_{product}"
                    coll_name = f"{formatted_date}_collection"

                    
                    # #handle Setting of Message to MongoDB
                    if check_daily_collection(workspace_id, product):
                            
                        response = data_cube.insert_data(api_key=api_key,db_name=db_name, coll_name=coll_name, data=message)
                        
                        if response['success'] == True:
                            sio.emit('ticket_message_response', {'data':"Message Send to DB", 'status': 'success', 'operation':'send_message'}, room=sid)
                            print(response)
                            # return 

                            # Commit the message offset to mark it as processed
                            self.consumer.commit()
                        else:
                            print(response)
                            return sio.emit('ticket_message_response', {'data':"Error sending message", 'status': 'failure', 'operation':'send_message'}, room=sid)

                    
                    
        except Exception as e:
            # Handle other exceptions
            error_message = str(e)
            print(error_message)
            # return sio.emit('public_room_response', {'data': error_message, 'status': 'failure', 'operation':'create_public_room'}, room=sid)
           
        finally:
        # Close down consumer to commit final offsets.
            self.consumer.close()