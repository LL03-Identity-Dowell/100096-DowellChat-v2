import json
import logging
import os
import sys
import threading
from confluent_kafka import Consumer
from confluent_kafka import KafkaError
from confluent_kafka import KafkaException
from datetime import date
from api.utils.datacube_utils import check_daily_collection, map_product_to_db, check_collection
from websocket.views import sio
from api.connector.database_connector import DataCubeConnection

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG to capture all logs
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)


# We want to run thread in an infinite loop
running = True
kafka_environ = os.getenv("ENVIRON")
conf = {'bootstrap.servers': f"{kafka_environ}:9092",
        'auto.offset.reset': 'smallest',
        'group.id': "user_group"}
# Topic
topic = 'ticket_chat_topic_test'

data_cube = DataCubeConnection()


class ChatCreatedListener(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # Create consumer
        self.consumer = Consumer(conf)
        logger.info("Initialized Kafka consumer.")

    def run(self):
        logger.info("Starting listener thread.")
        try:
            # Subcribe to topic
            self.consumer.subscribe([topic])
            while running:
                # Poll for message
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                # Handle Error
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        logger.warning('End of partition reached at offset %d', msg.offset())
                        # End of partition event
                        sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                         (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
                else:
                    # Handle Message
                    logger.info('Received message: %s', msg.value())
                    message = json.loads(msg.value().decode('utf-8'))
                    event_type = message.get('event_type')
                    data = message.get('data')

                    if event_type and data:
                        self.handle_event(event_type, data)

        except Exception as e:
            error_message = str(e)
            logger.exception("An error occurred: %s", e)
        finally:
            logger.info("Closing consumer.")
            self.consumer.close()


    def handle_event(self, event_type, data):
        handlers = {
            'create_topic': self.handle_create_topic,
            'ticket_message': self.handle_ticket_message,
            'create_linemanager':self.handle_create_linemanager,
        }
        handler = handlers.get(event_type)
        if handler:
            handler(data)

    def handle_ticket_message(self, data):
        workspace_id = data['workspace_id']
        product = data['product']
        api_key = data['api_key']


        # Removing of some keys
        unwanted_keys = ['workspace_id','product', 'api_key']

        for key in unwanted_keys:
            data.pop(key, None)

        formatted_date = str(date.today()).replace("-", "_")
        db_name = map_product_to_db(workspace_id, api_key, product)
        coll_name = f"{workspace_id}_{formatted_date}_{product}_collection"

        # handle Setting of Message to Datacube
        if check_daily_collection(api_key, workspace_id, product):

            response = data_cube.insert_data(
                api_key=api_key, db_name=db_name, coll_name=coll_name, data=data)

            if response['success'] == True:
                print("Message Sent to DataCube")
                print(response)
                # return

                # Commit the message offset to mark it as processed
                self.consumer.commit()
            else:
                print(response)

    def handle_create_topic(self, data):
        workspace_id = data['workspace_id']
        api_key = data['api_key']
        db_name = data['ddb_name']
        coll_name = f"{workspace_id}_topics"

        unwanted_keys = ['workspace_id','ddb_name', 'api_key']

        for key in unwanted_keys:
            data.pop(key, None)

        if check_collection(api_key, workspace_id, coll_name, db_name):
            response = data_cube.insert_data(api_key=api_key, db_name=db_name, coll_name=coll_name, data=data)

        if response['success']:
            print("Topic created successfully in DataCube")
            self.consumer.commit()
        else:
            print("Failed to create topic in DataCube")

    def handle_create_linemanager(self, data):
        workspace_id = data['workspace_id']
        api_key = data['api_key']
        db_name = data['db_name']
        coll_name = f"{workspace_id}_line_manager"

        unwanted_keys = ['workspace_id','db_name', 'api_key']

        for key in unwanted_keys:
            data.pop(key, None)

        if check_collection(api_key, workspace_id, coll_name, db_name):
            response = data_cube.insert_data(api_key=api_key, db_name=db_name, coll_name=coll_name, data=data)

        if response['success']:
            logger.info("Message sent to DataCube successfully.")
            print("Line Manager created successfully in DataCube")
            self.consumer.commit()
        else:
            logger.error("Failed to send message to DataCube: %s", response)