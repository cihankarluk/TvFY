from rest_framework import serializers

from TvFY.actor.models import Actor


class ActorListSerializer(serializers.ModelSerializer):
    born_at = serializers.CharField(source="actor_born_at")
    died_at = serializers.CharField(source="actor_died_at")

    class Meta:
        model = Actor
        fields = (
            "tvfy_code",
            "first_name",
            "last_name",
            "full_name",
            "imdb_url",
            "born_date",
            "born_at",
            "died_date",
            "died_at",
            "perks",
            "oscars",
            "oscar_nominations",
            "wins",
            "nominations",
        )
