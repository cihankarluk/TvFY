from TvFY.actor.models import Actor
from TvFY.core.models import Country, Language
from TvFY.genre.models import Genre
from TvFY.series.models import Episode, Season, Series, SeriesCast


class SeriesService:
    def __init__(self, search_data):
        self.search_data = search_data

    @property
    def get_genres(self):
        genres = set(self.search_data.get("rt_genre", {}))
        genres.update(set(self.search_data.get("imdb_genre", {})))
        genre_ids = Genre.objects.filter(name__in=genres).values_list("id", flat=True)
        return genre_ids

    @property
    def get_or_create_language(self):
        language_objs = []
        for language in self.search_data.get("language", []):
            language_obj, _ = Language.objects.get_or_create(language=language)
            language_objs.append(language_obj)
        return language_objs

    @property
    def get_or_create_country(self):
        country_objs = []
        for country in self.search_data.get("country", []):
            country_obj, _ = Country.objects.get_or_create(country=country)
            country_objs.append(country_obj)
        return country_objs

    @property
    def create_series(self):
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
        }

        series = Series.objects.create(**series_data)

        for genre in self.get_genres:
            series.genres.add(genre)
        for country in self.get_or_create_country:
            series.country.add(country)
        for language in self.get_or_create_language:
            series.language.add(language)

        return series


class SeriesCastService:
    def __init__(self, cast_data: list, series: Series):
        self.cast_data = cast_data
        self.series = series

    @staticmethod
    def get_or_create_actor(actor_data):
        actor, _ = Actor.objects.get_or_create(
            first_name=actor_data["first_name"], last_name=actor_data["last_name"]
        )
        return actor

    def create_series_cast(self):
        series_cast = []
        for cast in self.cast_data:
            actor = self.get_or_create_actor(cast)
            series_cast.append(
                SeriesCast(
                    character_name=cast["character_name"],
                    episode_count=cast["episode_count"],
                    start_acting=cast["start_acting"],
                    end_acting=cast["end_acting"],
                    series=self.series,
                    actor=actor,
                )
            )
        SeriesCast.objects.bulk_create(series_cast)


class SeasonEpisodeService:
    def __init__(self, search_data: dict, series: Series):
        self.search_data = search_data
        self.series = series

    def create_season_and_episodes(self):
        for season in range(1, self.search_data.get("seasons", 0) + 1):
            season_data = self.search_data[season]
            season = Season.objects.create(
                season=season, imdb_url=season_data[0]["imdb_url"], series=self.series
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
