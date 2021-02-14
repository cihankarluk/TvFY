import asyncio
import logging
from urllib.parse import urlparse

import aiohttp
import backoff
from bs4 import BeautifulSoup

from TvFY.collector.imdb import IMDBScrapper
from TvFY.collector.tomatoes import TomatoesScrapper

logger = logging.getLogger("main")


class Scrapper:
    def __init__(self, urls: list, search_type=None):
        self.urls = urls
        self.session = None
        self.search_type = search_type

    @staticmethod
    def scrapper_class(url, soup, search_type):
        scrapper_map = {
            "www.rottentomatoes.com": TomatoesScrapper,
            "www.imdb.com": IMDBScrapper,
        }
        base_url = urlparse(url).netloc
        if cls := scrapper_map.get(base_url):
            cls = cls(soup=soup[url], url=url, search_type=search_type)
        return cls

    @backoff.on_exception(
        backoff.expo, (aiohttp.ClientError, AssertionError), max_tries=2
    )
    async def fetch_html(self, url: str):
        search_response = await self.session.get(url)
        assert search_response.status == 200
        return search_response

    async def soup_response(self, url: str) -> dict:
        search_response = await self.fetch_html(url=url)
        text = await search_response.text()
        soup = BeautifulSoup(text, "html.parser")
        return {url: soup}

    async def weed_out(self, url: str):
        soup = await self.soup_response(url=url)
        cls = self.scrapper_class(url, soup, self.search_type)
        return cls.run()

    async def run(self):
        results = {}
        tasks = [self.weed_out(url=url) for url in self.urls]
        for task in asyncio.as_completed(tasks):
            result = await task
            results.update(result)
        return results

    async def main(self):
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False),
        ) as session:
            self.session = session
            response = await self.run()
            return response

    def handle(self):
        return asyncio.run(self.main())
