from django.urls import include, path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="TvFY API",
        default_version="v1",
        description="Simple API for scrap and serve.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="cihankarluk@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('account/', include('TvFY.user.urls'), name="account"),
    path("actor/", include("TvFY.actor.urls"), name="actor"),
    path("director/", include("TvFY.director.urls"), name="director"),
    path("movie/", include("TvFY.movies.urls"), name="movie"),
    path("series/", include("TvFY.series.urls"), name="series"),
    path("search/", include("TvFY.search.urls"), name="search"),
    path("country/", include("TvFY.country.urls"), name="country"),
    path("language/", include("TvFY.language.urls"), name="language"),
    path("genre/", include("TvFY.genre.urls"), name="genre"),

    # SWAGGER
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
