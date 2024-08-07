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
    
class TicketMessage(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    ticket_id = models.CharField(max_length=50)
    message_data = models.TextField(null=True)
    author = models.CharField(max_length=250)
    reply_to = models.CharField(max_length=250)
    is_read = models.BooleanField(default=False)
    created_at = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.room_id} - {self.author}'
    

class Workspace(models.Model):
    org_id = models.CharField(max_length=255, unique=True)
    api_key = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.org_id
    
class Topic(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    db_name = models.CharField(max_length=250, null=True, blank=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.workspace.org_id}"
    

class LineManager(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user_id = models.CharField(max_length=100)
    positions_in_a_line = models.PositiveIntegerField(default=0)
    average_serving_time = models.PositiveIntegerField(default=0)
    ticket_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} {self.workspace.org_id}"
    

class MetaSetting(models.Model):
    workspace = models.OneToOneField(Workspace, on_delete=models.CASCADE)
    waiting_time = models.PositiveIntegerField()
    operation_time = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.workspace.org_id