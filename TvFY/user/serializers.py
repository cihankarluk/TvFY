from rest_framework import serializers

from TvFY.series.models import Series, Season
from TvFY.series.serializers import EpisodeSerializer
from TvFY.user.models import UserMovies, UserSeries


class UserMovieCreateOrUpdateRequestSerializer(serializers.ModelSerializer):
    tvfy_code = serializers.CharField()

    class Meta:
        model = UserMovies
        fields = "tvfy_code", "is_watched", "is_going_to_watch",


class UserMovieCreateOrUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    movie_title = serializers.CharField(source="movie.title")

    class Meta:
        model = UserMovies
        fields = "user", "username", "movie", "movie_title", "is_watched", "is_going_to_watch",


class UserMovieSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source="movie.title")

    class Meta:
        model = UserMovies
        fields = "movie", "movie_title",


class UserMovieGetMoviesSerializer(serializers.Serializer):
    max_imdb_rate = serializers.FloatField()
    min_imdb_rate = serializers.FloatField()
    avg_imdb_rate = serializers.FloatField()
    max_rt_audience_rate = serializers.FloatField()
    min_rt_audience_rate = serializers.FloatField()
    avg_rt_audience_rate = serializers.FloatField()
    max_rt_tomatometer_rate = serializers.FloatField()
    min_rt_tomatometer_rate = serializers.FloatField()
    avg_rt_tomatometer_rate = serializers.FloatField()
    max_metacritic_score = serializers.FloatField()
    min_metacritic_score = serializers.FloatField()
    avg_metacritic_score = serializers.FloatField()
    newest_movie_watched = serializers.DateTimeField()
    oldest_movie_watched = serializers.DateTimeField()
    time_spent = serializers.FloatField()
    genres = serializers.ListField()
    countries = serializers.ListField()
    languages = serializers.ListField()
    watched_movies = UserMovieSerializer(many=True)
    watch_list = UserMovieSerializer(many=True)


class UserSeriesCreateOrUpdateRequestSerializer(serializers.ModelSerializer):
    tvfy_code = serializers.CharField()
    watched_past_seasons = serializers.BooleanField()

    class Meta:
        model = UserSeries
        fields = (
            "tvfy_code",
            "watched_season",
            "watched_past_seasons",
            "last_watched_episode",
            "is_watched",
            "is_going_to_watch",
        )


class UserSeriesCreateOrUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    series_title = serializers.CharField(source="series.title")
    watched_season = serializers.CharField(source="watched_season.season")

    class Meta:
        model = UserSeries
        fields = (
            "user",
            "username",
            "series_title",
            "watched_season",
            "last_watched_episode",
            "is_watched",
            "is_going_to_watch",
        )


class UserSeriesSeasonSerializer(serializers.ModelSerializer):
    episode_count = serializers.IntegerField(source="episode_set.count")
    avg_imdb_rate = serializers.FloatField(source="get_episodes_avg_imdb_rate")
    max_imdb_rate_episode = EpisodeSerializer(source="get_episodes_max_imdb_rate")
    min_imdb_rate_episode = EpisodeSerializer(source="get_episodes_min_imdb_rate")

    class Meta:
        model = Season
        fields = (
            "season",
            "episode_count",
            "imdb_url",
            "avg_imdb_rate",
            "max_imdb_rate_episode",
            "min_imdb_rate_episode",
        )


class UserSeriesSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = (
            "tvfy_code",
            "title",
            "is_active",
            "season_count",
            "wins",
            "oscar_wins",
            "imdb_rate",
            "rt_tomatometer_rate",
            "metacritic_score",
        )


class UserSeriesGetSeriesSerializer(serializers.Serializer):
    series = UserSeriesSeriesSerializer()
    last_watched_episode = serializers.CharField()
    watched_seasons = UserSeriesSeasonSerializer(many=True)
    unwatched_seasons = UserSeriesSeasonSerializer(many=True)
