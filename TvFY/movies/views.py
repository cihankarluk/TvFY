from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from TvFY.movies.models import Movie
from TvFY.movies.serializers import MovieListSerializer


class MovieViewSet(GenericViewSet, ListModelMixin):
    queryset = (
        Movie.objects.prefetch_related("genres", "country", "language")
        .select_related("director")
        .order_by("-created_at")
    )
    serializer_class = MovieListSerializer
    permission_classes = (AllowAny,)
