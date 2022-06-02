from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet

from TvFY.collector.base import Scraper
from TvFY.collector.google import GoogleScrapper
from TvFY.movies.models import Movie
from TvFY.movies.serializers import MovieListSerializer
from TvFY.movies.service import MovieService
from TvFY.search.serializers import SearchCreateSerializer
from TvFY.search.service import SearchService
from TvFY.series.models import Series
from TvFY.series.serializers import SeriesListSerializer
from TvFY.series.service import SeriesService


class SearchViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = SearchCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        valid_data = serializer.validated_data

        google_results = GoogleScrapper(search_key=valid_data["name"]).run()
        search_urls = SearchService.get_urls(google_data=google_results, search_type=valid_data["type"])
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
        return Response(serialized.data, status=HTTP_200_OK)
