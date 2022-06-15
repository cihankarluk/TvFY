from rest_framework import serializers

from TvFY.director.models import Director
from TvFY.movies.models import Movie
from TvFY.series.models import Series


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


class DirectorMovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = (
            "tvfy_code",
            "title",
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
            "metacritic_score",
        )


class DirectorSeriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Series
        fields = (
            "tvfy_code",
            "title",
            "storyline",
            "release_date",
            "end_date",
            "run_time",
            "is_active",
            "season_count",
            "wins",
            "nominations",
            "oscar_wins",
            "oscar_nominations",
            "tv_network",
            "imdb_rate",
            "imdb_vote_count",
            "imdb_popularity",
            "imdb_url",
            "rt_tomatometer_rate",
            "rt_audience_rate",
            "rotten_tomatoes_url",
            "metacritic_score",
        )


class DirectorDetailSerializer(serializers.ModelSerializer):
    born_at = serializers.CharField(source="director_born_at")
    died_at = serializers.CharField(source="director_died_at")
    director_movie = DirectorMovieSerializer(source="movie_set.all", read_only=True, many=True)
    director_series = DirectorSeriesSerializer(source="series_set.all", read_only=True, many=True)

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
            "director_movie",
            "director_series",
        )
