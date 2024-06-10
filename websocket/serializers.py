from rest_framework import serializers
from .models import Room, Message

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class MessageSerializer(serializers.Serializer):
    type = serializers.CharField(allow_null=False, allow_blank=False) 
    room_id = serializers.CharField(allow_null=False, allow_blank=False)
    message_data = serializers.CharField(allow_null=False, allow_blank=False)
    side = serializers.CharField(allow_null=False, allow_blank=False)
    author = serializers.CharField(allow_null=False, allow_blank=False)
    message_type = serializers.CharField(allow_null=False, allow_blank=False)