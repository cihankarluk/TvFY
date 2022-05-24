from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from TvFY.language.models import Language
from TvFY.language.serializers import LanguageListSerializer


class LanguageViewSet(GenericViewSet, ListModelMixin):
    queryset = Language.objects.all()
    serializer_class = LanguageListSerializer
    filter_backends = SearchFilter,
    search_fields = "name",
