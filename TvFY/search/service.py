from typing import Union
from urllib.parse import urljoin

from TvFY.collector.base import Scraper
from TvFY.collector.imdb import IMDBBase
from TvFY.core.exceptions import SourceUrlNotFound
from TvFY.movies.models import Movie
from TvFY.movies.serializers import MovieListSerializer
from TvFY.movies.service import MovieService
from TvFY.series.models import Series
from TvFY.series.serializers import SeriesListSerializer
from TvFY.series.service import SeriesService


class SearchService:
    @classmethod
    def get_urls(cls, google_data: dict[str, str], search_type: str) -> list[str]:
        urls = []
        if imdb_base := google_data.get("imdb_url"):
            urls.append(urljoin(imdb_base, IMDBBase.CAST))
            if search_type == Series.TYPE:
                urls.append(f"{urljoin(imdb_base, IMDBBase.EPISODES)}?season=1")
            urls.append(imdb_base)
        if rottentomatoes := google_data.get("rotten_tomatoes_url"):
            urls.append(rottentomatoes)
        return urls

    @classmethod
    def check_source_url_exists(cls, google_results: dict[str, str], valid_data: dict[str, str]):
        if not (google_results.get("imdb_url") or google_results.get("rotten_tomatoes_url")):
            raise SourceUrlNotFound(f"Source url not found for {valid_data['name']}.")

    @classmethod
    def scrap(
        cls,
        valid_data: dict[str, str],
        search_urls: list[str],
        google_results: dict[str, str],
    ) -> Union[SeriesListSerializer, MovieListSerializer]:
        if valid_data["type"] == Series.TYPE:
            scrapping_cls = Scraper(urls=search_urls, search_type=Series.TYPE)
            results = scrapping_cls.handle()
            results.update(google_results)
            object_ = SeriesService.create_or_update_series(search_data=results)
            serialized = SeriesListSerializer(object_)
        else:
            scrapping_cls = Scraper(urls=search_urls, search_type=Movie.TYPE)
            results = scrapping_cls.handle()
            results.update(google_results)
            object_ = MovieService.create_or_update_movie(search_data=results)
            serialized = MovieListSerializer(object_)

        return serialized
