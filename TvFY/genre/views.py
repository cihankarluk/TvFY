from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from TvFY.genre.models import Genre
from TvFY.genre.serializers import GenreListSerializer


class GenreViewSet(GenericViewSet, ListModelMixin):
    serializer_class = GenreListSerializer
    queryset = Genre.objects.all()
    filter_backends = SearchFilter,
    search_fields = "name",
