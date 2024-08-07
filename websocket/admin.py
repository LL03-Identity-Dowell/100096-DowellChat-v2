from django.contrib import admin
from .models import Workspace, Topic, TicketMessage, LineManager, MetaSetting

admin.site.register(Workspace)
admin.site.register(Topic)
admin.site.register(TicketMessage)
admin.site.register(LineManager)
admin.site.register(MetaSetting)