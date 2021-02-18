from rest_framework import generics

from TvFY.actor.models import Actor
from TvFY.actor.serializers import ActorSerializer


class ActorView(generics.ListAPIView):
    serializer_class = ActorSerializer
    queryset = Actor.objects.select_related("born_at", "died_at")
