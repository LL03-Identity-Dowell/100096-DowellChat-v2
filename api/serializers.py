from rest_framework import serializers


class MasterLinkSerializer(serializers.Serializer):
    number_of_links = serializers.IntegerField()
    product_distribution = serializers.JSONField()
    usernames = serializers.ListField()
    workspace_id = serializers.CharField(allow_null=True, allow_blank=True) 
    api_key = serializers.CharField(allow_null=False, allow_blank=False)
    created_at = serializers.CharField(allow_null=False, allow_blank=False)
