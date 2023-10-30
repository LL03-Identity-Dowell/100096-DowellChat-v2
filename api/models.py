from django.db import models
import uuid

# Create your models here.

class Room(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    room_name = models.CharField(max_length=250, null=True)
    org_id = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.room_name


class Message(models.Model):
    type = models.CharField(max_length=50, null=True)
    room_id = models.CharField(max_length=50, null=True)
    message_data = models.TextField(null=True)
    side = models.CharField(max_length=50, null=True)
    author = models.CharField(max_length=250, null=True)
    message_type = models.CharField(max_length=50, null=True)

    
    def __str__(self):
        return f'{self.room_id} - {self.author}'