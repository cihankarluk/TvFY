from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from TvFY.series.models import Series
from TvFY.series.serializers import SeriesListSerializer, SeriesDetailSerializer, SeriesCastSerializer


class SeriesViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = (
        Series.objects.prefetch_related(
            "seriescast_set__actor", "genres", "country", "language"
        ).select_related(
            "creator"
        ).order_by("-created_at")
    )
    serializer_class = SeriesListSerializer
    permission_classes = AllowAny,
    filter_backends = DjangoFilterBackend, OrderingFilter, SearchFilter,
    search_fields = "title", "=tvfy_code",
    ordering_fields = "imdb_rate", "wins", "nominations",
    lookup_field = "tvfy_code"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SeriesDetailSerializer
        elif self.action == "get_cast":
            return SeriesCastSerializer
        return self.serializer_class

    def retrieve(self, request, *args, **kwargs):
        series: Series = self.get_object()

        serializer = self.get_serializer(series)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["get"],
        detail=True,
        url_path="cast",
        url_name="cast",
    )
    def get_cast(self, request, *args, **kwargs):
        series: Series = self.get_object()
        series_cast = series.seriescast_set.all()

        serializer = self.get_serializer(series_cast, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
