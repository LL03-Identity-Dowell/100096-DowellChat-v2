from django.core.management.base import BaseCommand
from api.kafka_consumer import ChatCreatedListener
class Command(BaseCommand):
    help = 'Launches Listener for ticket chat message : Kafka'
    def handle(self, *args, **options):
        td = ChatCreatedListener()
        td.start()
        self.stdout.write("Started Consumer Thread")