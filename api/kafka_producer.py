import json
from confluent_kafka import Producer
import socket
import os

kafka_environ = os.getenv("ENVIRON")

class ProducerTicketChat:
    def __init__(self) -> None:        
        conf = {'bootstrap.servers': f"{kafka_environ}:9092",'client.id': socket.gethostname()}
        self.producer = Producer(conf)
        self.topic='ticket_chat_topic_test'

    # This method will be called inside view for sending Kafka message
    def publish(self, body):
        print('Sending to Kafka: ')
        self.producer.produce(self.topic, key="key.chat.created", value=json.dumps(body))
        # # Flush and close the producer
        self.producer.flush()

class ProducerCreateTicket:
    def __init__(self) -> None:        
        conf = {'bootstrap.servers': f"{kafka_environ}:9092",'client.id': socket.gethostname()}
        self.producer = Producer(conf)
        self.topic='ticket_topic_test'

    # This method will be called inside view for sending Kafka message
    def publish(self, body):
        print('Sending to Kafka: ')
        self.producer.produce(self.topic, key="key.chat.created", value=json.dumps(body))
        # # Flush and close the producer
        self.producer.flush()