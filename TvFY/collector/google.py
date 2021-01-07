import re
from collections import OrderedDict

import requests
from bs4 import BeautifulSoup


class GoogleScrapper:
    def __init__(self, search_key):
        self.search_key = search_key

    def google_search(self):
        search_url = f"https://www.google.com/search?q={self.search_key}&hl=en-EN"
        search_response = requests.get(search_url)
        soup = BeautifulSoup(search_response.content, "lxml")
        return soup

    @staticmethod
    def regex_search(content: str, pattern: str) -> str:
        try:
            string = re.search(pattern, content).group()
        except AttributeError:
            string = None
        return string

    def get_imdb_url(self, content: str) -> dict:
        regex_pattern = r"https://www.imdb.com/title/[^;]*/"
        imdb_url = self.regex_search(content=content, pattern=regex_pattern)
        result = {"imdb_url": imdb_url} if imdb_url else {}
        return result

    def get_rotten_tomatoes_url(self, content: str) -> dict:
        regex_pattern = r"https://www.rottentomatoes.com/.+?/.+?(?<=/)"
        rotten_tomatoes_url = self.regex_search(content=content, pattern=regex_pattern)
        result = (
            {"rotten_tomatoes_url": rotten_tomatoes_url} if rotten_tomatoes_url else {}
        )
        return result

    def get_imdb_rate(self, content: str) -> dict:
        regex_pattern = r"(\d.\d|\d)/10\s.\sIMDb"
        imdb_rate = self.regex_search(content, regex_pattern)
        result = {"imdb_rate": imdb_rate} if imdb_rate else {}
        return result

    def get_rotten_tomatoes_rate(self, content: str) -> dict:
        regex_pattern = r"\d{1,2}%\s.\sRotten\sTomatoes"
        rotten_tomatoes_rate = self.regex_search(content=content, pattern=regex_pattern)
        result = (
            {"rotten_tomatoes_rate": rotten_tomatoes_rate}
            if rotten_tomatoes_rate
            else {}
        )
        return result

    def get_tv_com_rate(self, content: str) -> dict:
        regex_pattern = r"(\d.\d|\d)/10\s.\sTV.com"
        tv_com_rate = self.regex_search(content=content, pattern=regex_pattern)
        result = {"tv_com_rate": tv_com_rate} if tv_com_rate else {}
        return result

    def get_dates(self, content: str) -> dict:
        regex_pattern = r"Original\srelease:\s\w{1,9}\s\d{1,2},\s\d{1,4}\s\W;\s(present|\w{1,9}\s\d{1,2},\s\d{1,4})"  # noqa
        reg_search = self.regex_search(content=content, pattern=regex_pattern)
        if not reg_search:
            return {}

        # ['Original release: July 26, 2019 –', ' July 26, 2020']
        date_list = reg_search.split(";")

        release_date = date_list[0].split(":")[-1].replace("–", "").strip()
        end_date = date_list[-1].strip()
        is_active = end_date == "present"
        # 'July 26, 2019'
        result = {
            "release_date": release_date,
            "is_active": is_active,
            "end_date": end_date if not is_active else None,
        }
        return result

    def get_seasons(self, content):
        regex_pattern = r"(No.\sof\sseasons:\s\d{1,3})|(\d{1,2}\sseasons)"
        reg_search = self.regex_search(content=content, pattern=regex_pattern)
        if reg_search:
            try:
                _, seasons = reg_search.split(":")
            except ValueError:
                seasons, _ = reg_search.split(" ")
        else:
            seasons = None
        result = {"seasons": seasons.strip()} if seasons else {}
        return result

    def run_method(self, action: str, content: str):
        action_class: dict = OrderedDict(
            [
                ("get_imdb_url", self.get_imdb_url),
                ("get_rotten_tomatoes_url", self.get_rotten_tomatoes_url),
                ("get_imdb_rate", self.get_imdb_rate),
                ("get_rotten_tomatoes_rate", self.get_rotten_tomatoes_rate),
                ("get_tv_com_rate", self.get_tv_com_rate),
                ("get_dates", self.get_dates),
                ("get_seasons", self.get_seasons)
            ]
        )
        action_method: classmethod = action_class[action]
        return action_method(content=content)

    def search_divs(self, soup):
        actions = [
            "get_imdb_rate",
            "get_rotten_tomatoes_rate",
            "get_tv_com_rate",
            "get_dates",
            "get_seasons"
        ]
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
