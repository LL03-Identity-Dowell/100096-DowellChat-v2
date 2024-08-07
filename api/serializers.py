from rest_framework import serializers
from .models import MasterLink
from websocket.models import Workspace


class MasterLinkSerializer(serializers.ModelSerializer):
    workspace_id = serializers.CharField(write_only=True)
    api_key = serializers.CharField(write_only=True)
    
    class Meta:
        model = MasterLink
        fields = '__all__'
        read_only_fields = ('master_link', 'link_id', 'available_links', 'workspace')
