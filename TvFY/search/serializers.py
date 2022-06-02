from rest_framework import serializers


class SearchCreateSerializer(serializers.Serializer):
    type = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
