import asyncio
import logging
import aiohttp
from bs4 import BeautifulSoup

logger = logging.getLogger('main')


class Scrapper:
    def __init__(self, urls):
        self.urls = urls
        self.session = None

    async def fetch_html(self, url: str):
        search_response = await self.session.get(url)
        try:
            assert search_response.status == 200
        except (aiohttp.ClientError, AssertionError) as e:
            logging.exception(e)
            return await self.fetch_html(url)
        return search_response

    async def soup_response(self, url):
        search_response = await self.fetch_html(url=url)
        text = await search_response.text()
        soup = BeautifulSoup(text, "lxml")
        return {url: soup}

    async def run(self):
        results = []
        tasks = [self.soup_response(url=url) for url in self.urls]
        for task in asyncio.as_completed(tasks):
            soup = await task
            results.append(soup)
        return results

    async def main(self):
        async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=False),
        ) as session:
            self.session = session
            return await self.run()

    def handle(self):
        return asyncio.run(self.main())
