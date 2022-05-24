from rest_framework import serializers

from TvFY.language.models import Language


class LanguageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"
