from django.contrib import admin
from .models import Workspace, Topic, TicketMessage

admin.site.register(Workspace)
admin.site.register(Topic)
admin.site.register(TicketMessage)