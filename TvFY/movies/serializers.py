from rest_framework import serializers

from TvFY.actor.serializers import ActorListSerializer
from TvFY.movies.models import Movie, MovieCast


class MovieCastSerializer(serializers.ModelSerializer):
    actor = ActorListSerializer(read_only=True)

    class Meta:
        model = MovieCast
        fields = (
            "character_name",
            "actor",
        )


class MovieListSerializer(serializers.ModelSerializer):
    director = serializers.SerializerMethodField("get_full_name")
    genres = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    country = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    language = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

    class Meta:
        model = Movie
        fields = (
            "tvfy_code",
            "title",
            "storyline",
            "release_date",
            "run_time",
            "rt_tomatometer_rate",
            "rt_audience_rate",
            "imdb_popularity",
            "imdb_rate",
            "imdb_vote_count",
            "wins",
            "nominations",
            "budget",
            "budget_currency",
            "usa_opening_weekend",
            "usa_opening_weekend_currency",
            "ww_gross",
            "imdb_url",
            "rotten_tomatoes_url",
            "director",
            "genres",
            "country",
            "language",
        )

    @classmethod
    def get_full_name(cls, obj):
        full_name = obj.director and obj.director.full_name
        return full_name


class MovieDetailSerializer(MovieListSerializer):
    cast = MovieCastSerializer(source="moviecast_set.all", read_only=True, many=True)

    class Meta:
        model = Movie
        fields = (
            "tvfy_code",
            "title",
            "storyline",
            "release_date",
            "run_time",
            "rt_tomatometer_rate",
            "rt_audience_rate",
            "imdb_popularity",
            "imdb_rate",
            "imdb_vote_count",
            "wins",
            "nominations",
            "budget",
            "budget_currency",
            "usa_opening_weekend",
            "usa_opening_weekend_currency",
            "ww_gross",
            "imdb_url",
            "rotten_tomatoes_url",
            "director",
            "genres",
            "country",
            "language",
            "cast",
        )
