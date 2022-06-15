from typing import Union, List, Optional

import requests
from bs4 import BeautifulSoup
from django.test import TestCase
from model_bakery import baker

from TvFY.actor.models import Actor
from TvFY.collector.base import Scraper
from TvFY.collector.google import GoogleScrapper
from TvFY.collector.imdb import IMDBBase
from TvFY.collector.tomatoes import RottenTomatoesBase
from TvFY.director.models import Director
from TvFY.series.models import Series, SeriesCast, Season, Episode


class BaseTestCase(TestCase):
    @classmethod
    def get_imdb_result(cls, url: str, search_type: str) -> dict:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        cls_ = IMDBBase(soup=soup, url=url, search_type=search_type)
        result = cls_.run()
        return result

    @classmethod
    def get_tomatoes_result(cls, url: str, search_type: str) -> dict:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        cls_ = RottenTomatoesBase(soup=soup, url=url, search_type=search_type)
        result = cls_.run()
        return result

    @classmethod
    def get_google_result(cls, search_key: str) -> dict:
        cls_ = GoogleScrapper(search_key=search_key)
        result = cls_.run()
        return result

    @classmethod
    def get_scrapper_result(cls, urls: List[str], search_type: str) -> dict:
        cls_ = Scraper(urls=urls, search_type=search_type)
        result = cls_.handle()
        return result

    @classmethod
    def is_subset(cls, attrs: set, results: Union[dict, list]) -> bool:
        """
        Take diff of expected attrs and results from scrapping if diff are
         different from the expected attrs returns False.
        """
        if isinstance(results, dict):
            results = [results]
        is_subset = all([all([attrs - set(result.keys()), set(result.keys()) - attrs]) for result in results])
        return not is_subset

    @classmethod
    def take_diff(cls, attrs: set, results: Union[dict, list[dict]]) -> list:
        if isinstance(results, dict):
            results = [results]

        differences = []
        for item in results:
            differences.extend(list(attrs - set(item.keys())))
        return differences

    # MODELS

    @classmethod
    def create_actor(
            cls,
            first_name="",
            last_name="",
            full_name="",
            imdb_url="https://www.test.com/name/",
            born_date=None,
            born_at=None,
            died_date=None,
            died_at=None,
            perks=None,
            oscars=None,
            oscar_nominations=None,
            wins=None,
            nominations=None,
            is_updated=False,
    ) -> Actor:
        actor = baker.make(
            Actor,
            first_name=first_name,
            last_name=last_name,
            full_name=full_name,
            imdb_url=imdb_url,
            born_date=born_date,
            born_at=born_at,
            died_date=died_date,
            died_at=died_at,
            perks=perks,
            oscars=oscars,
            oscar_nominations=oscar_nominations,
            wins=wins,
            nominations=nominations,
            is_updated=is_updated,
        )
        return actor

    @classmethod
    def create_director(
            cls,
            first_name="",
            last_name="",
            full_name="",
            imdb_url="https://www.test.com/name/",
            rt_url=None,
            born_date=None,
            born_at=None,
            died_date=None,
            died_at=None,
            perks=None,
            oscars=None,
            oscar_nominations=None,
            wins=None,
            nominations=None,
            is_updated=False,
    ) -> Director:
        director = baker.make(
            Director,
            first_name=first_name,
            last_name=last_name,
            full_name=full_name,
            imdb_url=imdb_url,
            rt_url=rt_url,
            born_date=born_date,
            born_at=born_at,
            died_date=died_date,
            died_at=died_at,
            perks=perks,
            oscars=oscars,
            oscar_nominations=oscar_nominations,
            wins=wins,
            nominations=nominations,
            is_updated=is_updated,
        )
        return director

    @classmethod
    def create_series(
            cls,
            title=None,
            storyline=None,
            release_date=None,
            end_date=None,
            run_time=None,
            is_active=None,
            season_count=None,
            wins=None,
            nominations=None,
            oscar_wins=None,
            oscar_nominations=None,
            tv_network=None,
            imdb_rate=None,
            imdb_vote_count=None,
            imdb_popularity=None,
            imdb_url=None,
            rt_tomatometer_rate=None,
            rt_audience_rate=None,
            rotten_tomatoes_url=None,
            metacritic_score=None,
            creator=None,
    ) -> Series:
        series = baker.make(
            Series,
            title=title or f"{title}_{imdb_url}",
            storyline=storyline,
            release_date=release_date,
            end_date=end_date,
            run_time=run_time,
            is_active=is_active,
            season_count=season_count,
            wins=wins,
            nominations=nominations,
            oscar_wins=oscar_wins,
            oscar_nominations=oscar_nominations,
            tv_network=tv_network,
            imdb_rate=imdb_rate,
            imdb_vote_count=imdb_vote_count,
            imdb_popularity=imdb_popularity,
            imdb_url=imdb_url,
            rt_tomatometer_rate=rt_tomatometer_rate,
            rt_audience_rate=rt_audience_rate,
            rotten_tomatoes_url=rotten_tomatoes_url or f"{rotten_tomatoes_url}",
            metacritic_score=metacritic_score,
            creator=creator,
        )
        return series

    @classmethod
    def create_series_cast(
            cls,
            character_name="",
            episode_count=None,
            start_acting=None,
            end_acting=None,
            series=None,
            actor=None,
    ) -> SeriesCast:
        series_cast = baker.make(
            SeriesCast,
            character_name=character_name,
            episode_count=episode_count,
            start_acting=start_acting,
            end_acting=end_acting,
            series=series or cls.create_series(),
            actor=actor or cls.create_actor(),
        )
        return series_cast

    @classmethod
    def create_season(
            cls,
            season=None,
            imdb_url=None,
            imdb_season_average_rate=None,
            series=None,
    ) -> Season:
        season = baker.make(
            Season,
            season=season,
            imdb_url=imdb_url,
            imdb_season_average_rate=imdb_season_average_rate,
            series=series or cls.create_series(),
        )
        return season

    @classmethod
    def create_episode(
            cls,
            title=None,
            storyline=None,
            release_date=None,
            imdb_rate=None,
            imdb_vote_count=None,
            episode=None,
            season=None,
    ) -> Episode:
        episode = baker.make(
            Episode,
            title=title,
            storyline=storyline,
            release_date=release_date,
            imdb_rate=imdb_rate,
            imdb_vote_count=imdb_vote_count,
            episode=episode,
            season=season or cls.create_season(),
        )
        return episode

