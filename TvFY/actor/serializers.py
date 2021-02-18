from rest_framework import serializers

from TvFY.actor.models import Actor


class ActorSerializer(serializers.ModelSerializer):
    actor_born_at = serializers.ReadOnlyField()
    actor_died_at = serializers.ReadOnlyField()

    class Meta:
        model = Actor
        fields = (
            "first_name",
            "last_name",
            "imdb_url",
            "born_date",
            "actor_born_at",
            "died_date",
            "actor_died_at",
            "perks",
            "oscars",
            "oscar_nominations",
            "wins",
            "nominations",
        )

    def to_representation(self, instance: Actor):
        data = super(ActorSerializer, self).to_representation(instance)
        data["full_name"] = instance.get_full_name
        return data
