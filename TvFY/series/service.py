from typing import Optional

from TvFY.actor.service import ActorService
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
        SeriesCastService.bulk_create_series_cast(search_data=search_data, series=series)

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
            "season_count": search_data.get("seasons"),
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
    def bulk_create_series_cast(cls, search_data: dict, series: Series):
        cast_data = search_data.get("cast", [])
        actor_dict = ActorService.create_multiple_actor(cast_data=cast_data)

        series_cast = []
        for cast in cast_data:
            series_cast.append(
                SeriesCast(
                    character_name=cast["character_name"],
                    episode_count=cast["episode_count"],
                    start_acting=cast["start_acting"],
                    end_acting=cast["end_acting"],
                    series=series,
                    actor=actor_dict[cast["imdb_actor_url"]]["actor"],
                )
            )
        SeriesCast.objects.bulk_create(series_cast)


class SeriesSeasonEpisodeService:

    @classmethod
    def create_season_and_episodes(cls, series: Series, search_data: dict):
        for season in range(1, search_data.get("seasons", 0) + 1):
            season_data = search_data[season]
            season = Season.objects.create(
                season=season,
                imdb_url=season_data[0]["imdb_url"],
                series=series,
            )
            for episode in season_data:
                # TODO: bulk create
                Episode.objects.create(
                    name=episode["name"],
                    storyline=episode.get("storyline"),
                    release_date=episode.get("release_date"),
                    imdb_rate=episode.get("imdb_rate"),
                    imdb_vote_count=episode.get("imdb_vote_count"),
                    episode=episode.get("episode"),
                    season=season,
                )
