from typing import Union, List

import requests
from bs4 import BeautifulSoup
from django.test import TestCase
from model_bakery import baker

from TvFY.actor.models import Actor
from TvFY.collector.base import Scraper
from TvFY.collector.google import GoogleScrapper
from TvFY.collector.imdb import IMDBBase
from TvFY.collector.tomatoes import TomatoesBase
from TvFY.director.models import Director


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
        cls_ = TomatoesBase(soup=soup, url=url, search_type=search_type)
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

