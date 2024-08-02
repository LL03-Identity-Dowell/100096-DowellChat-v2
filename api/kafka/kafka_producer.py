import json
from confluent_kafka import Producer
import socket
import os

kafka_environ = os.getenv("ENVIRON")

class ProducerTicketChat:
    def __init__(self) -> None:        
        conf = {'bootstrap.servers': "kafka:9092",'client.id': socket.gethostname()}
        self.producer = Producer(conf)
        self.topic='ticket_chat_topic_test'

    # This method will be called inside view for sending Kafka message
    def publish(self, body):
        print('Sending to Kafka: ')
        self.producer.produce(self.topic, key="key.chat.created", value=json.dumps(body))
        # # Flush and close the producer
        self.producer.flush()

class ProducerAllEvents:
    def __init__(self) -> None:        
        conf = {'bootstrap.servers': "kafka:9092",'client.id': socket.gethostname()}
        self.producer = Producer(conf)
        self.topic='ticket_chat_topic_test'

    # This method will be called inside view for sending Kafka message
    def publish(self, body, event_type):
        print('Sending to Kafka: ')
        message = {
            'event_type': event_type,
            'data': body
        }
        self.producer.produce(self.topic, key="key.chat.created", value=json.dumps(message))
        # Flush and close the producer
        self.producer.flush()
