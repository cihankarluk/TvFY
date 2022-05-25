from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from TvFY.director.models import Director
from TvFY.director.serializers import DirectorListSerializer


class DirectorViewSet(GenericViewSet, ListModelMixin):
    serializer_class = DirectorListSerializer
    queryset = Director.objects.select_related("born_at", "died_at")
    filter_backends = SearchFilter,
    search_fields = "full_name",
