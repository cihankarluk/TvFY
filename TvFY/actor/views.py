from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from TvFY.actor.models import Actor
from TvFY.actor.serializers import ActorListSerializer


class ActorViewSet(GenericViewSet, ListModelMixin):
    serializer_class = ActorListSerializer
    queryset = Actor.objects.select_related("born_at", "died_at")
    filter_backends = SearchFilter,
    search_fields = "full_name",
