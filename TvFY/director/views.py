from django.http import Http404
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from TvFY.core.exceptions import DirectorNotFoundError
from TvFY.director.models import Director
from TvFY.director.serializers import DirectorListSerializer, DirectorDetailSerializer


class DirectorViewSet(GenericViewSet, ListModelMixin):
    queryset = (
        Director.objects.prefetch_related(
            "movie_set", "series_set"
        ).select_related(
            "born_at", "died_at"
        ).order_by("-created_at")
    )
    serializer_class = DirectorListSerializer
    filter_backends = SearchFilter,
    search_fields = "full_name",
    lookup_field = "tvfy_code"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DirectorDetailSerializer
        return self.serializer_class

    def get_object(self):
        try:
            director = super(DirectorViewSet, self).get_object()
        except Http404:
            raise DirectorNotFoundError(f"Director with {self.kwargs['tvfy_code']} code does not exists.")
        return director

    def retrieve(self, request, *args, **kwargs):
        director: Director = self.get_object()

        serializer = self.get_serializer(director)

        return Response(serializer.data, status=status.HTTP_200_OK)
