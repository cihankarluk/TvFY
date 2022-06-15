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
            "wins",
            "nominations",
            "oscar_wins",
            "oscar_nominations",
            "run_time",
            "imdb_rate",
            "imdb_vote_count",
            "imdb_popularity",
            "imdb_url",
            "rt_tomatometer_rate",
            "rt_tomatometer_count",
            "rt_audience_rate",
            "rt_audience_count",
            "rotten_tomatoes_url",
            "budget_amount",
            "budget_currency",
            "usa_ow_amount",
            "usa_ow_currency",
            "ww_amount",
            "ww_currency",
            "metacritic_score",
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
            "wins",
            "nominations",
            "oscar_wins",
            "oscar_nominations",
            "run_time",
            "imdb_rate",
            "imdb_vote_count",
            "imdb_popularity",
            "imdb_url",
            "rt_tomatometer_rate",
            "rt_tomatometer_count",
            "rt_audience_rate",
            "rt_audience_count",
            "rotten_tomatoes_url",
            "budget_amount",
            "budget_currency",
            "usa_ow_amount",
            "usa_ow_currency",
            "ww_amount",
            "ww_currency",
            "metacritic_score",
            "director",
            "genres",
            "country",
            "language",
            "cast",
        )
