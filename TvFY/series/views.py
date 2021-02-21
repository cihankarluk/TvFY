from rest_framework import generics

from TvFY.core.exceptions import SeriesDoesNotExist
from TvFY.series.models import Series
from TvFY.series.serializers import SeriesDetailSerializer, SeriesSerializer


class SeriesView(generics.ListAPIView):
    serializer_class = SeriesSerializer
    queryset = Series.objects.all()


class SeriesDetailView(generics.RetrieveAPIView):
    serializer_class = SeriesDetailSerializer

    def get_object(self):
        tvfy_code = self.kwargs.get("tvfy_code")
        try:
            series = Series.objects.get(tvfy_code=tvfy_code)
        except Series.DoesNotExist:
            raise SeriesDoesNotExist("Series does not exists.")
        return series
