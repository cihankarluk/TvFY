from rest_framework import serializers

from TvFY.country.models import Country


class CountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"
