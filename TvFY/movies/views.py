from django.db.models import F, Value
from django.db.models.functions import Concat
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from TvFY.movies.filters import MovieViewSetFilterSet
from TvFY.movies.models import Movie
from TvFY.movies.serializers import MovieListSerializer


class MovieViewSet(GenericViewSet, ListModelMixin):
    queryset = (
        Movie.objects.prefetch_related("genres", "country", "language")
        .select_related("director")
        .order_by("-created_at")
        .annotate(
            director_full_name=Concat(
                F("director__first_name"), Value(" "), F("director__last_name")
            ),
        )
    )
    serializer_class = MovieListSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_class = MovieViewSetFilterSet
    search_fields = (
        "title",
        "tvfy_code",
        "director__get_full_name",
    )
    ordering_fields = (
        "created_at",
        "imdb_rate",
        "wins",
        "nominations",
    )
