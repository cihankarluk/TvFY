from rest_framework import serializers

from TvFY.director.models import Director


class DirectorSerializer(serializers.ModelSerializer):
    director_born_at = serializers.ReadOnlyField()
    director_died_at = serializers.ReadOnlyField()

    class Meta:
        model = Director
        fields = (
            "first_name",
            "last_name",
            "imdb_url",
            "rt_url",
            "born_date",
            "director_born_at",
            "died_date",
            "director_died_at",
            "perks",
            "oscars",
            "oscar_nominations",
            "wins",
            "nominations",
        )

    def to_representation(self, instance: Director):
        data = super(DirectorSerializer, self).to_representation(instance)
        data["full_name"] = instance.get_full_name
        return data
