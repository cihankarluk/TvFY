from rest_framework import serializers

from TvFY.director.models import Director


class DirectorListSerializer(serializers.ModelSerializer):
    born_at = serializers.CharField(source="director_born_at")
    died_at = serializers.CharField(source="director_died_at")

    class Meta:
        model = Director
        fields = (
            "tvfy_code",
            "first_name",
            "last_name",
            "full_name",
            "imdb_url",
            "rt_url",
            "born_at",
            "born_date",
            "died_at",
            "died_date",
            "perks",
            "oscars",
            "oscar_nominations",
            "wins",
            "nominations",
        )
