from rest_framework import generics

from TvFY.director.models import Director
from TvFY.director.serializers import DirectorSerializer


class DirectorView(generics.ListAPIView):
    serializer_class = DirectorSerializer
    queryset = Director.objects.select_related("born_at", "died_at")
