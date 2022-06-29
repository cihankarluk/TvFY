from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from TvFY.country.models import Country
from TvFY.country.serializers import CountryListSerializer


class CountryViewSet(GenericViewSet, ListModelMixin):
    queryset = Country.objects.all()
    serializer_class = CountryListSerializer
    filter_backends = (SearchFilter,)
    search_fields = ("name",)
