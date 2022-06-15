import requests

from TvFY.core.helpers import regex_search


class GoogleScrapper:
    def __init__(self, search_key):
        self.search_key = search_key

    @property
    def google_search(self) -> str:
        search_url = f"https://www.google.com/search?q={self.search_key}&hl=en-EN"
        search_response = requests.get(search_url)
        return search_response.text

    @staticmethod
    def get_imdb_url(content: str) -> dict:
        regex_pattern = r"https://www.imdb.com/title/[^;]*/"
        imdb_url = regex_search(content=content, pattern=regex_pattern)
        result = {"imdb_url": imdb_url} if imdb_url else {}
        return result

    @classmethod
    def get_rotten_tomatoes_url(cls, content: str, u_rotten_tomatoes_url=None) -> dict:
        result = {}

        regex_pattern = r"https://www.rottentomatoes.com/(.*?)&"
        rotten_tomatoes_url = regex_search(content=content, pattern=regex_pattern)
        if rotten_tomatoes_url:
            rotten_tomatoes_url = rotten_tomatoes_url[:len(rotten_tomatoes_url) - 1]
            result = {"rotten_tomatoes_url": rotten_tomatoes_url}

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

    def run(self) -> dict:
        content = self.google_search
        result = {}
        result.update(self.get_imdb_url(content))
        result.update(self.get_rotten_tomatoes_url(content))
        result.update(self.get_tv_com_rate(content))
        # result.update(self.get_seasons(content))
        return result
