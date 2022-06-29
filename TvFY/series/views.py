from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from TvFY.core.exceptions import SeriesNotFoundError
from TvFY.series.models import Series
from TvFY.series.serializers import SeriesListSerializer, SeriesDetailSerializer, SeriesCastSerializer, \
    SeriesSeasonSerializer, EpisodeSerializer


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
        elif self.action == "get_seasons":
            return SeriesSeasonSerializer
        elif self.action == "season_episodes":
            return EpisodeSerializer
        return self.serializer_class

    def get_object(self):
        try:
            series = super(SeriesViewSet, self).get_object()
        except Http404:
            raise SeriesNotFoundError(f"Series with {self.kwargs['tvfy_code']} code does not exists.")
        return series

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

    @action(
        methods=["get"],
        detail=True,
        url_path="season",
        url_name="season",
    )
    def get_seasons(self, request, *args, **kwargs):
        series: Series = self.get_object()
        series_seasons = series.season_set.all()

        serializer = self.get_serializer(series_seasons, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["get"],
        detail=True,
        url_path="season/(?P<season_id>[^/.]+)",
        url_name="season_episodes"
    )
    def season_episodes(self, request, *args, **kwargs):
        series: Series = self.get_object()

        season_obj = get_object_or_404(series.season_set.all(), **{"season": kwargs["season_id"]})
        episodes = season_obj.episode_set.order_by("episode").all()

        serializer = self.get_serializer(episodes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
