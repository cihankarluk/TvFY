from rest_framework import serializers

from TvFY.actor.serializers import ActorListSerializer
from TvFY.series.models import Series, SeriesCast, Season, Episode


class SeriesCastSerializer(serializers.ModelSerializer):
    actor = ActorListSerializer(read_only=True)

    class Meta:
        model = SeriesCast
        fields = (
            "character_name",
            "episode_count",
            "start_acting",
            "end_acting",
            "actor",
        )


class SeriesListSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField("get_full_name")
    genres = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    country = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    language = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

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
            "creator",
            "genres",
            "country",
            "language",
        )

    @classmethod
    def get_full_name(cls, obj):
        full_name = obj.creator and obj.creator.full_name
        return full_name


class SeriesDetailSerializer(SeriesListSerializer):
    cast = SeriesCastSerializer(source="seriescast_set.all", read_only=True, many=True)

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
            "creator",
            "genres",
            "country",
            "language",
            "cast",
        )


class SeriesSeasonSerializer(serializers.ModelSerializer):
    series_title = serializers.CharField(source="series.title")

    class Meta:
        model = Season
        fields = (
            "season",
            "imdb_url",
            "imdb_season_average_rate",
            "series_title",
        )


class SeriesSeasonEpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = (
            "tvfy_code",
            "title",
            "storyline",
            "release_date",
            "imdb_rate",
            "imdb_vote_count",
            "episode",
        )
