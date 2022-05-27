import django_filters

from TvFY.movies.models import Movie


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class MovieViewSetFilterSet(django_filters.FilterSet):
    release_date = django_filters.DateFromToRangeFilter()
    run_time = django_filters.RangeFilter()
    rt_tomatometer_rate = django_filters.RangeFilter()
    rt_audience_rate = django_filters.RangeFilter()
    imdb_rate = django_filters.RangeFilter()
    imdb_popularity = django_filters.RangeFilter()
    wins = django_filters.RangeFilter()
    nominations = django_filters.RangeFilter()

    director_full_name = django_filters.CharFilter(field_name="director__full_name", lookup_expr="icontains")

    genres = NumberInFilter(distinct=True)
    country = NumberInFilter(distinct=True)
    language = NumberInFilter(distinct=True)

    class Meta:
        model = Movie
        fields = (
            "imdb_rate",
            "imdb_popularity",
            "wins",
            "nominations",
            "release_date",
            "genres",
        )
