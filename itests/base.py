import requests
from bs4 import BeautifulSoup
from django.test import TestCase

from TvFY.collector.imdb import IMDBBase


class BaseTestCase(TestCase):
    @classmethod
    def get_imdb_result(cls, url, search_type):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        cls_ = IMDBBase(soup=soup, url=url, search_type=search_type)
        result = cls_.run()
        return result

    @classmethod
    def is_subset(cls, attrs, results) -> bool:
        return all(set(attrs).issubset(transaction) for transaction in results)