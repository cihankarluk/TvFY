from rest_framework import serializers

from TvFY.genre.models import Genre


class GenreListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = (
            "name",
            "detail",
        )
