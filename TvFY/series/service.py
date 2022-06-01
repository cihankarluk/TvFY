from typing import Optional, List
from urllib.parse import urljoin

from django.db.models import QuerySet

from TvFY.actor.models import Actor
from TvFY.actor.service import ActorService
from TvFY.collector.base import Scraper
from TvFY.collector.imdb import IMDBBase
from TvFY.core.exceptions import NotAbleToFindSeriesSourceUrl
from TvFY.country.service import CountryService
from TvFY.director.service import DirectorService
from TvFY.genre.service import GenreService
from TvFY.language.service import LanguageService
from TvFY.series.models import Episode, Season, Series, SeriesCast


class SeriesService:

    @classmethod
    def check_source_urls(cls, search_data: dict) -> None:
        """
        At least one of them concur to find data about that movie.
        """
        if not (search_data.get("imdb_url") or search_data.get("rotten_tomatoes_url")):
            raise NotAbleToFindSeriesSourceUrl(
                "Cannot find source url for that series. If you know address please contact."
            )
        return None

    @classmethod
    def get_series(cls, filter_map: dict) -> Optional[Series]:
        series_query = Series.objects.filter(**filter_map)
        if series_query.exists():
            series = series_query.get()
        else:
            series = None
        return series

    @classmethod
    def check_series_exists(cls, search_data: dict) -> Optional[Series]:
        if imdb_url := search_data.get("imdb_url"):
            movie = cls.get_series(filter_map={"imdb_url": imdb_url})
        elif rotten_tomatoes_url := search_data.get("rotten_tomatoes_url"):
            movie = cls.get_series(filter_map={"rotten_tomatoes_url": rotten_tomatoes_url})
        else:
            movie = None
        return movie

    @classmethod
    def create_series(cls, series_data: dict, search_data: dict) -> Series:
        series = Series.objects.create(**series_data)
        for genre in GenreService.get_genre_ids(search_data=search_data):
            series.genres.add(genre)
        for country in CountryService.get_or_create_multiple_country(search_data=search_data):
            series.country.add(country)
        for language in LanguageService.get_or_create_multiple_language(search_data=search_data):
            series.language.add(language)
        SeriesCastService.create_or_update_series_cast(series=series, search_data=search_data)
        SeriesSeasonEpisodeService.create_or_update_series_season_episodes(
            series=series, search_data=search_data, season_number="1"
        )

        return series

    @classmethod
    def update_series(cls, series: Series, series_data: dict) -> Series:
        for field, value in series_data.items():
            setattr(series, field, value)
        series.save()
        return series

    @classmethod
    def create_or_update_series(cls, search_data: dict) -> Series:
        series_data = {
            "title": search_data["title"],
            "storyline": search_data.get("storyline"),
            "release_date": search_data.get("release_date"),
            "end_date": search_data.get("end_date"),
            "run_time": search_data.get("run_time"),
            "is_active": search_data.get("is_active"),
            "season_count": search_data.get("season_count"),
            "wins": search_data.get("wins"),
            "nominations": search_data.get("nominations"),
            "tv_network": search_data.get("network"),
            "imdb_rate": search_data.get("total_imdb_rate"),
            "imdb_vote_count": search_data.get("imdb_vote_count"),
            "imdb_popularity": search_data.get("imdb_popularity"),
            "imdb_url": search_data.get("imdb_url"),
            "rt_tomatometer_rate": search_data.get("rt_tomatometer_rate"),
            "rt_audience_rate": search_data.get("rt_audience_rate"),
            "rotten_tomatoes_url": search_data.get("rotten_tomatoes_url"),
            "tv_com_rate": search_data.get("tv_com_rate"),
            "tv_com_url": search_data.get("tv_com_url"),
            "creator": DirectorService.get_or_create_director(search_data=search_data),
        }

        if series := cls.check_series_exists(search_data=search_data):
            series = cls.update_series(series=series, series_data=series_data)
        else:
            series = cls.create_series(series_data=series_data, search_data=search_data)

        return series


class SeriesCastService:

    @classmethod
    def create_series_cast(cls, series: Series, actor: Actor, cast_data: dict) -> SeriesCast:
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
    def update_series_cast(cls, series_cast: SeriesCast, cast_data: dict):
        for field, value in cast_data.items():
            setattr(series_cast, field, value)
        series_cast.save()

    @classmethod
    def get_series_cast_query(cls, series: Series, cast_data_list: List[dict], actor_map: dict) -> QuerySet:
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
    def create_or_update_series_cast(cls, series: Series, search_data: dict):
        cast_data_list = search_data.get("cast", [])
        actor_map = ActorService.create_multiple_actor(cast_data=cast_data_list)
        series_cast_query = cls.get_series_cast_query(series=series, cast_data_list=cast_data_list, actor_map=actor_map)

        series_cast_objects = []
        for cast_data in cast_data_list:
            actor = actor_map[cast_data["imdb_actor_url"]]["actor"]
            if series_cast := series_cast_query.filter(actor=actor):
                cls.update_series_cast(series_cast=series_cast.first(), cast_data=cast_data)
            else:
                series_cast_objects.append(cls.create_series_cast(series=series, actor=actor, cast_data=cast_data))

        if series_cast_objects:
            SeriesCast.objects.bulk_create(series_cast_objects)


class SeriesSeasonEpisodeService:

    @classmethod
    def create_episode(cls, season: Season, episode_data: dict) -> Episode:
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
    def update_episode(cls, episode: Episode, episode_data: dict):
        for field, value, in episode_data.items():
            setattr(episode, field, value)
        episode.save()

    @classmethod
    def get_episode_query(cls, season: Season, season_data: List[dict]) -> QuerySet:
        episode_names = [episode_data["title"] for episode_data in season_data]
        episode_query = Episode.objects.filter(season=season, title__in=episode_names)
        return episode_query

    @classmethod
    def create_or_update_series_season_episodes(cls, series: Series, search_data: dict, season_number: str):
        for value in list(search_data.keys()):
            if season_number in value:
                season_data = search_data[value][season_number]
                season, _ = Season.objects.get_or_create(
                    season=season_number,
                    imdb_url=season_data[0]["imdb_url"],
                    series=series,
                )

                episodes = []
                episode_query = cls.get_episode_query(season=season, season_data=season_data)
                for episode_data in season_data:
                    if episode := episode_query.filter(title=episode_data["title"]):
                        cls.update_episode(episode=episode.first(), episode_data=episode_data)
                    else:
                        episodes.append(cls.create_episode(season=season, episode_data=episode_data))

                if episodes:
                    Episode.objects.bulk_create(episodes)

    @classmethod
    def scrap_and_update_episodes(cls):
        series_query = Series.objects.all()

        series_map = {
            series.season_count: series
            for series in series_query
            if series.season_count != series.season_set.count()
        }

        url_map = {}
        for key, value in series_map.items():
            for i in range(2, key + 1):
                url_map[f"{urljoin(value.imdb_url, IMDBBase.EPISODES)}?season={i}"] = None

        results = Scraper(urls=list(url_map.keys())).handle()

        for imdb_url, search_result in results.items():
            for key, value in search_result.items():
                if isinstance(value, list):
                    if value:
                        series = Series.objects.get(imdb_url=f"{imdb_url.rsplit('/', 1)[0]}/")
                        cls.create_or_update_series_season_episodes(
                            series=series,
                            search_data=search_result,
                            season_number=key
                        )
