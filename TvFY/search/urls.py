from TvFY.core.routers import RestRouter
from TvFY.search.views import SearchViewSet

router = RestRouter()

router.register("", SearchViewSet, basename="search")

urlpatterns = router.urls
