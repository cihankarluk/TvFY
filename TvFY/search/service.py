from urllib.parse import urljoin

from TvFY.collector.imdb import IMDBBase
from TvFY.series.models import Series


class SearchService:

    @classmethod
    def get_urls(cls, google_data: dict[str, str], search_type) -> list[str]:
        urls = []
        if imdb_base := google_data.get("imdb_url"):
            urls.append(urljoin(imdb_base, IMDBBase.CAST))
            urls.append(urljoin(imdb_base, IMDBBase.AWARDS))
            if search_type == Series.TYPE:
                urls.append(f"{urljoin(imdb_base, IMDBBase.EPISODES)}?season=1")
            urls.append(imdb_base)
        if rottentomatoes := google_data.get("rotten_tomatoes_url"):
            urls.append(rottentomatoes)
        return urls
