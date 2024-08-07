from django.db import models
import uuid
from websocket.models import Workspace


# Create your models here.

class MasterLink(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    link_id = models.CharField(max_length=250, unique=True)
    number_of_links = models.PositiveIntegerField()
    available_links = models.PositiveIntegerField()
    product_distribution = models.JSONField()
    usernames = models.JSONField()
    is_active = models.BooleanField(default=True)
    link = models.URLField(max_length=1000, null=True, blank=True)
    master_link = models.URLField(max_length=500)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.link_id
