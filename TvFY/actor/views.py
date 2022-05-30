from django.http import Http404
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from TvFY.actor.models import Actor
from TvFY.actor.serializers import ActorListSerializer, ActorDetailSerializer
from TvFY.core.exceptions import ActorNotFoundError


class ActorViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = (
        Actor.objects.prefetch_related(
            "seriescast_set", "moviecast_set"
        ).select_related(
            "born_at", "died_at"
        ).order_by("-created_at")
    )
    serializer_class = ActorListSerializer
    filter_backends = SearchFilter,
    search_fields = "full_name",
    lookup_field = "tvfy_code"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ActorDetailSerializer
        return self.serializer_class

    def get_object(self):
        try:
            actor = super(ActorViewSet, self).get_object()
        except Http404:
            raise ActorNotFoundError(f"Actor with {self.kwargs['tvfy_code']} code does not exists.")
        return actor

    def retrieve(self, request, *args, **kwargs):
        actor: Actor = self.get_object()

        serializer = self.get_serializer(actor)

        return Response(serializer.data, status=status.HTTP_200_OK)
