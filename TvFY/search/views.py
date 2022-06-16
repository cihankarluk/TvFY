from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet

from TvFY.collector.google import GoogleScrapper
from TvFY.search.serializers import SearchCreateSerializer
from TvFY.search.service import SearchService


class SearchViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = SearchCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        valid_data = serializer.validated_data

        google_results = GoogleScrapper(search_key=valid_data["name"]).run()
        SearchService.check_source_url_exists(google_results=google_results, valid_data=valid_data)

        search_urls = SearchService.get_urls(google_data=google_results, search_type=valid_data["type"])
        serialized = SearchService.scrap(valid_data=valid_data, search_urls=search_urls, google_results=google_results)

        return Response(serialized.data, status=HTTP_200_OK)
