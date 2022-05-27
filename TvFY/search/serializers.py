from rest_framework import serializers


class SearchGetOrCreateSerializer(serializers.Serializer):
    type = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
