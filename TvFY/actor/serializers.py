from rest_framework import serializers

from TvFY.actor.models import Actor


class ActorListSerializer(serializers.ModelSerializer):
    born_at = serializers.SerializerMethodField(method_name="get_born_at")
    died_at = serializers.SerializerMethodField(method_name="get_died_at")

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

    @classmethod
    def get_born_at(cls, obj):
        return obj.born_at and obj.born_at.name

    @classmethod
    def get_died_at(cls, obj):
        return obj.died_at and obj.died_at.name
