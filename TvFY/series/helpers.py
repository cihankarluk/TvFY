from TvFY.series.models import Episode, Season, Series, SeriesCast


class SaveSeriesData:
    def __init__(self, search_data):
        self.search_data = search_data

    def save_data(self):
        series_data = {
            "name": self.search_data["title"],
            "creator": self.search_data.get("creator"),
            "storyline": self.search_data.get("storyline"),
            "tv_network": self.search_data.get("network"),
            "rt_tomatometer": self.search_data.get("rt_tomatometer"),
            "rt_audience_rate": self.search_data.get("rt_audience_rate"),
            "release_date": self.search_data.get("release_date"),
            "run_time": self.search_data.get("run_time"),
            "imdb_popularity": self.search_data.get("popularity"),
            "wins": self.search_data.get("wins"),
            "nominations": self.search_data.get("nominations"),
            "is_active": self.search_data.get("is_active"),
            "imdb_url": self.search_data.get("imdb_url"),
            "rotten_tomatoes_url": self.search_data.get("rotten_tomatoes_url"),
            "end_date": self.search_data.get("end_date"),
            "imdb_rate": self.search_data.get("total_imdb_rate"),
            "imdb_vote_count": self.search_data.get("total_imdb_vote_count"),
            "season_count": self.search_data.get("seasons"),
            "rt_genre": self.search_data.get("rt_genre"),
            "imdb_genre": self.search_data.get("imdb_genre"),
            "language": self.search_data.get("language"),
            "country": self.search_data.get("country"),
        }

        series = Series.objects.save_series(**series_data)
        cast_data = self.search_data.get("cast", [])
        SeriesCast.objects.save_series_cast(cast_data=cast_data, series=series)

        for season in range(1, self.search_data.get("seasons", 0) + 1):
            season_data = self.search_data[season]
            season = Season.objects.create(
                season=season, imdb_url=season_data[0]["imdb_url"], series=series
            )
            for episode in season_data:
                Episode.objects.create(
                    name=episode["name"],
                    storyline=episode.get("storyline"),
                    release_date=episode.get("release_date"),
                    imdb_rate=episode.get("imdb_rate"),
                    imdb_vote_count=episode.get("imdb_vote_count"),
                    episode=episode.get("episode"),
                    season=season,
                )
