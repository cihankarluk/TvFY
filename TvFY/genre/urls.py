from TvFY.core.routers import RestRouter
from TvFY.genre.views import GenreViewSet

router = RestRouter()

router.register("", GenreViewSet, basename="genre")

urlpatterns = router.urls
