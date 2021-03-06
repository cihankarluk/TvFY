from collections import OrderedDict

import requests
from bs4 import BeautifulSoup

from TvFY.core.helpers import regex_search


class GoogleScrapper:
    def __init__(self, search_key):
        self.search_key = search_key

    def google_search(self):
        search_url = f"https://www.google.com/search?q={self.search_key}&hl=en-EN"
        search_response = requests.get(search_url)
        soup = BeautifulSoup(search_response.content, "lxml")
        return soup

    @staticmethod
    def get_imdb_url(content: str) -> dict:
        regex_pattern = r"https://www.imdb.com/title/[^;]*/"
        imdb_url = regex_search(content=content, pattern=regex_pattern)
        result = {"imdb_url": imdb_url} if imdb_url else {}
        return result

    @staticmethod
    def get_rotten_tomatoes_url(content: str) -> dict:
        regex_pattern = r"https://www.rottentomatoes.com/.+?/.+?(?<=/)"
        rotten_tomatoes_url = regex_search(content=content, pattern=regex_pattern)
        result = (
            {"rotten_tomatoes_url": rotten_tomatoes_url} if rotten_tomatoes_url else {}
        )
        return result

    @staticmethod
    def get_tv_com_rate(content: str) -> dict:
        regex_pattern = r"(\d.\d|\d)/10\s.\sTV.com"
        tv_com_rate = regex_search(content=content, pattern=regex_pattern)
        result = {"tv_com_rate": tv_com_rate} if tv_com_rate else {}
        return result

    @staticmethod
    def get_seasons(content):
        regex_pattern = r"(No.\sof\sseasons:\s\d{1,3})|(\d{1,2}\sseasons)"
        reg_search = regex_search(content=content, pattern=regex_pattern)
        if reg_search:
            try:
                _, seasons = reg_search.split(":")
            except ValueError:
                seasons, _ = reg_search.split(" ")
        else:
            seasons = None
        result = {"seasons": int(seasons.strip())} if seasons else {}
        return result

    def run_method(self, action: str, content: str):
        action_class: dict = OrderedDict(
            [
                ("get_imdb_url", self.get_imdb_url),
                ("get_rotten_tomatoes_url", self.get_rotten_tomatoes_url),
                ("get_tv_com_rate", self.get_tv_com_rate),
                ("get_seasons", self.get_seasons),
            ]
        )
        action_method: classmethod = action_class[action]
        return action_method(content=content)

    def search_divs(self, soup):
        actions = ["get_tv_com_rate", "get_seasons"]
        repeat, result = None, {}
        for div in soup.find_all("div"):
            if (content := div.text) == repeat or not content:
                repeat = content
                continue
            for index, action in enumerate(actions):
                if data := self.run_method(action, content):
                    actions.pop(index)
                    result.update(data)
            if not actions:
                break
        return result

    def search_urls(self, soup):
        actions = ["get_imdb_url", "get_rotten_tomatoes_url"]
        repeat, result = None, {}
        for div in soup.find_all("a", href=True):
            if (content := div["href"]) == repeat or not content:
                repeat = content
                continue
            for index, action in enumerate(actions):
                if data := self.run_method(action, content):
                    actions.pop(index)
                    result.update(data)
            if not actions:
                break
        return result

    def run(self):
        soup = self.google_search()
        result = self.search_divs(soup)
        result.update(self.search_urls(soup))
        return result
