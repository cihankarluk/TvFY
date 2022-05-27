from TvFY.core.routers import RestRouter
from TvFY.series.views import SeriesViewSet

router = RestRouter()

router.register("", SeriesViewSet, basename="series")

urlpatterns = router.urls
