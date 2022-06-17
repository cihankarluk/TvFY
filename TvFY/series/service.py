from typing import Optional, List, Any
from urllib.parse import urljoin

from django.db.models import QuerySet

from TvFY.actor.models import Actor
from TvFY.actor.service import ActorService
from TvFY.collector.base import Scraper
from TvFY.collector.imdb import IMDBBase
from TvFY.country.service import CountryService
from TvFY.director.service import DirectorService
from TvFY.genre.service import GenreService
from TvFY.language.service import LanguageService
from TvFY.series.models import Episode, Season, Series, SeriesCast


class SeriesService:

    @classmethod
    def prepare_series_data(cls, search_data: dict[str, Any]) -> dict[str, Any]:
        series_data = {}

        if imdb_url := search_data.get("imdb_url"):
            series_data.update(search_data[imdb_url])  # IMDB data for that movie
            series_data.update(search_data[f"{imdb_url}fullcredits"])  # CAST
            series_data["imdb_url"] = imdb_url
            series_data["season=1"] = search_data[f"{imdb_url}episodes?season=1"]
        if rt_url := search_data.get("rotten_tomatoes_url"):
            series_data.update(search_data[rt_url])
            series_data["rotten_tomatoes_url"] = rt_url

        return series_data

    @classmethod
    def get_series(cls, filter_map: dict[str, Any]) -> Optional[Series]:
        series = None
        series_query = Series.objects.filter(**filter_map)
        if series_query.exists():
            series = series_query.get()

        return series

    @classmethod
    def check_series_exists(cls, series_data: dict[str, Any]) -> Optional[Series]:
        series = None
        if imdb_url := series_data.get("imdb_url"):
            series = cls.get_series(filter_map={"imdb_url": imdb_url})
        elif rotten_tomatoes_url := series_data.get("rotten_tomatoes_url"):
            series = cls.get_series(filter_map={"rotten_tomatoes_url": rotten_tomatoes_url})

        return series

    @classmethod
    def create_series_model_data(cls, series_data: dict[str, Any]) -> dict[str, Any]:
        """
        Prepare data for series model.
        """
        movie_model_data = {
            "title": series_data.get("imdb_title") or series_data.get("rt_title"),
            "storyline": series_data.get("rt_storyline"),
            "release_date": series_data.get("release_date"),
            "end_date": series_data.get("end_date"),
            "run_time": series_data.get("run_time"),
            "is_active": series_data.get("is_active"),
            "season_count": series_data.get("season_count"),
            "wins": series_data.get("wins"),
            "nominations": series_data.get("nominations"),
            "oscar_wins": series_data.get("oscar_wins"),
            "oscar_nominations": series_data.get("oscar_nominations"),
            "tv_network": series_data.get("network"),
            "imdb_rate": series_data.get("imdb_rate"),
            "imdb_vote_count": series_data.get("imdb_vote_count"),
            "imdb_popularity": series_data.get("imdb_popularity"),
            "rt_tomatometer_rate": series_data.get("rt_tomatometer_rate"),
            "rt_audience_rate": series_data.get("rt_audience_rate"),
            "metacritic_score": series_data.get("metacritic_score"),
            "imdb_url": series_data.get("imdb_url"),
            "rotten_tomatoes_url": series_data.get("rotten_tomatoes_url"),
            "creator": DirectorService.get_or_create_director(search_data=series_data),
        }
        return movie_model_data

    @classmethod
    def update_series(cls, series: Series, series_data: dict[str, Any]) -> Series:
        series_model_data = cls.create_series_model_data(series_data=series_data)
        for field, value in series_model_data.items():
            setattr(series, field, value)
        series.save()

        return series

    @classmethod
    def create_series(cls, series_data: dict[str, Any]) -> Series:
        series_model_data = cls.create_series_model_data(series_data=series_data)
        series = Series.objects.create(**series_model_data)
        for genre in GenreService.get_genre_ids(search_data=series_data):
            series.genres.add(genre)
        for country in CountryService.get_or_create_multiple_country(search_data=series_data):
            series.country.add(country)
        for language in LanguageService.get_or_create_multiple_language(search_data=series_data):
            series.language.add(language)
        SeriesCastService.create_or_update_series_cast(series=series, series_data=series_data)
        SeriesSeasonEpisodeService.create_or_update_series_season_episodes(
            series=series, search_data=series_data["season=1"],
        )

        return series

    @classmethod
    def create_or_update_series(cls, search_data: dict[str, Any]) -> Series:
        series_data = cls.prepare_series_data(search_data=search_data)

        if series := cls.check_series_exists(series_data=series_data):
            series = cls.update_series(series=series, series_data=series_data)
        else:
            series = cls.create_series(series_data=series_data)

        return series


class SeriesCastService:

    @classmethod
    def get_series_cast_query(
            cls, series: Series, cast_data_list: List[dict], actor_map: dict[str, dict[str, Any]]
    ) -> QuerySet:
        """
        Filter SeriesCast objects to later decide create or update.
        """
        character_names = [cast_data["character_name"] for cast_data in cast_data_list]
        series_cast_query = SeriesCast.objects.filter(
            series=series,
            character_name__in=character_names,
            actor__imdb_url__in=list(actor_map.keys())
        )

        return series_cast_query

    @classmethod
    def update_series_cast(cls, series_cast: SeriesCast, cast_data: dict[str, Any]):
        for field, value in cast_data.items():
            setattr(series_cast, field, value)
        series_cast.save()

    @classmethod
    def create_series_cast(cls, series: Series, actor: Actor, cast_data: dict[str, Any]) -> SeriesCast:
        series_cast = SeriesCast(
            character_name=cast_data["character_name"],
            episode_count=cast_data["episode_count"],
            start_acting=cast_data.get("start_acting"),
            end_acting=cast_data.get("end_acting"),
            series=series,
            actor=actor,
        )

        return series_cast

    @classmethod
    def create_or_update_series_cast(cls, series: Series, series_data: dict[str, Any]):
        cast_data_list = series_data.get("cast", [])
        actor_map = ActorService.create_multiple_actor(cast_data=cast_data_list)
        series_cast_query = cls.get_series_cast_query(series=series, cast_data_list=cast_data_list, actor_map=actor_map)

        series_cast_objects = []
        for cast_data in cast_data_list:
            actor = actor_map[cast_data["imdb_actor_url"]]["actor"]
            if series_cast := series_cast_query.filter(actor=actor):
                cls.update_series_cast(series_cast=series_cast.get(), cast_data=cast_data)
            else:
                series_cast_objects.append(cls.create_series_cast(series=series, actor=actor, cast_data=cast_data))

        if series_cast_objects:
            SeriesCast.objects.bulk_create(series_cast_objects)


class SeriesSeasonEpisodeService:

    @classmethod
    def get_episode_query(cls, season: Season, season_data: List[dict[str, Any]]) -> QuerySet:
        episode_names = [episode_data["title"] for episode_data in season_data]
        episode_query = Episode.objects.filter(season=season, title__in=episode_names)

        return episode_query

    @classmethod
    def update_episode(cls, episode: Episode, episode_data: dict[str, Any]):
        for field, value, in episode_data.items():
            setattr(episode, field, value)
        episode.save()

    @classmethod
    def create_episode(cls, season: Season, episode_data: dict[str, Any]) -> Episode:
        episode = Episode(
            title=episode_data["title"],
            storyline=episode_data.get("storyline"),
            release_date=episode_data.get("release_date"),
            imdb_rate=episode_data.get("imdb_rate"),
            imdb_vote_count=episode_data.get("imdb_vote_count"),
            episode=episode_data.get("episode"),
            season=season,
        )

        return episode

    @classmethod
    def create_or_update_series_season_episodes(cls, series: Series, search_data: dict[str, Any]):
        for season_number, season_data in search_data.items():
            season, _ = Season.objects.get_or_create(
                season=season_number,
                imdb_url=season_data[0]["imdb_url"],
                series=series,
            )

            episodes = []
            episode_query = cls.get_episode_query(season=season, season_data=season_data)
            for episode_data in season_data:
                if episode := episode_query.filter(title=episode_data["title"]):
                    cls.update_episode(episode=episode.get(), episode_data=episode_data)
                else:
                    episodes.append(cls.create_episode(season=season, episode_data=episode_data))

            if episodes:
                Episode.objects.bulk_create(episodes)

    @classmethod
    def scrap_and_update_episodes(cls):
        series_query = Series.objects.prefetch_related("season_set").all()

        series_list = [
            (series.imdb_url, series.season_count)
            for series in series_query
            if series.season_count != series.season_set.count()
        ]

        url_map = {}
        for series_url, season_count in series_list:
            for index in range(2, season_count + 1):
                url_map[f"{urljoin(series_url, IMDBBase.EPISODES)}?season={index}"] = None

        results = Scraper(urls=list(url_map.keys())).handle()

        for imdb_url, search_result in results.items():
            for key, value in search_result.items():
                if value and isinstance(value, list):
                    series = Series.objects.get(imdb_url=f"{imdb_url.rsplit('/', 1)[0]}/")
                    cls.create_or_update_series_season_episodes(
                        series=series,
                        search_data=search_result,
                    )
