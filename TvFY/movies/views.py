from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from TvFY.core.exceptions import MovieNotFoundError
from TvFY.movies.filters import MovieViewSetFilterSet
from TvFY.movies.models import Movie
from TvFY.movies.serializers import MovieCastSerializer, MovieDetailSerializer, MovieListSerializer


class MovieViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = (
        Movie.objects.prefetch_related("genres", "country", "language")
        .select_related("director")
        .order_by("-created_at")
    )
    serializer_class = MovieListSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_class = MovieViewSetFilterSet
    search_fields = (
        "title",
        "=tvfy_code",
        "director__full_name",
    )
    ordering_fields = (
        "created_at",
        "imdb_rate",
        "wins",
        "nominations",
    )
    lookup_field = "tvfy_code"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return MovieDetailSerializer
        elif self.action == "get_cast":
            return MovieCastSerializer
        return self.serializer_class

    def get_object(self):
        try:
            movie = super().get_object()
        except Http404:
            raise MovieNotFoundError(f"Movie with {self.kwargs['tvfy_code']} code does not exists.")
        return movie

    def retrieve(self, request, *args, **kwargs):
        """Return detailed movie data."""
        movie: Movie = self.get_object()

        serializer = self.get_serializer(movie)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["get"],
        detail=True,
        url_path="cast",
        url_name="cast",
    )
    def get_cast(self, request, *args, **kwargs):
        movie: Movie = self.get_object()
        movie_cast = movie.moviecast_set.all()

        serializer = self.get_serializer(movie_cast, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
