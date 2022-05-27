from typing import List
from urllib.parse import urljoin

from TvFY.collector.imdb import IMDBBase


class SearchService:

    @classmethod
    def get_urls(cls, google_data: dict) -> List[str]:
        urls = []
        if imdb_base := google_data.get("imdb_url"):
            urls.append(urljoin(imdb_base, IMDBBase.CAST))
            urls.append(urljoin(imdb_base, IMDBBase.AWARDS))
            urls.append(imdb_base)
        if rottentomatoes := google_data.get("rotten_tomatoes_url"):
            urls.append(rottentomatoes)
        return urls
