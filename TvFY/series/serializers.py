from rest_framework import serializers

from TvFY.series.models import Series


class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = (
            "tvfy_code",
            "name",
            "release_date",
            "is_active",
            "tv_network",
            "imdb_rate",
            "tv_com_rate",
            "rt_tomatometer",
            "rt_audience_rate",
            "tvfy_rate",
            "tvfy_popularity",
        )


class SeriesDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = (
            "tvfy_code",
            "name",
            "creator",
            "run_time",
            "storyline",
            "release_date",
            "is_active",
            "end_date",
            "tv_network",
            "wins",
            "nominations",
            "season_count",
            "imdb_rate",
            "imdb_vote_count",
            "imdb_popularity",
            "tv_com_rate",
            "rt_tomatometer",
            "rt_audience_rate",
            "tvfy_rate",
            "tvfy_popularity",
            "imdb_url",
            "imdb_creator_url",
            "tv_network_url",
            "rotten_tomatoes_url",
        )
