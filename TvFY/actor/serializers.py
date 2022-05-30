from rest_framework import serializers

from TvFY.actor.models import Actor
from TvFY.movies.models import MovieCast
from TvFY.series.models import SeriesCast


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


class ActorMovieCastSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source="movie.title")

    class Meta:
        model = MovieCast
        fields = "character_name", "movie_title"


class ActorSeriesCastSerializer(serializers.ModelSerializer):
    series_title = serializers.CharField(source="series.title")

    class Meta:
        model = SeriesCast
        fields = "character_name", "series_title", "episode_count", "start_acting", "end_acting"


class ActorDetailSerializer(serializers.ModelSerializer):
    movie_cast = ActorMovieCastSerializer(source="moviecast_set.all", read_only=True, many=True)
    series_cast = ActorSeriesCastSerializer(source="seriescast_set.all", read_only=True, many=True)

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
            "movie_cast",
            "series_cast",
        )
