import requests
from bs4 import BeautifulSoup
from django.test import TestCase

from TvFY.collector.base import Scrapper
from TvFY.collector.google import GoogleScrapper
from TvFY.collector.imdb import IMDBBase
from TvFY.collector.tomatoes import TomatoesBase


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
    def get_scrapper_result(cls, urls: list, search_type: str) -> dict:
        cls_ = Scrapper(urls=urls, search_type=search_type)
        result = cls_.handle()
        return result

    @classmethod
    def is_subset(cls, attrs, results) -> bool:
        set_attrs = set(attrs)
        is_subset: bool = all(
            set_attrs.issubset(transaction) and set_attrs.issuperset(transaction)
            for transaction in results
        )
        return is_subset
