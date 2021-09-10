from TvFY.core.routers import RestRouter
from TvFY.movies.views import MovieViewSet

router = RestRouter()

router.register("", MovieViewSet, basename="movie")

urlpatterns = router.urls
