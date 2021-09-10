from rest_framework import serializers

from TvFY.movies.models import Movie


class MovieListSerializer(serializers.ModelSerializer):
    director = serializers.CharField(source="director.get_full_name")
    genres = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    country = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="country"
    )
    language = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="language"
    )

    class Meta:
        model = Movie
        fields = (
            "id",
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
