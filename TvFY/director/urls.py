from TvFY.core.routers import RestRouter
from TvFY.director.views import DirectorViewSet

router = RestRouter()

router.register("", DirectorViewSet, basename="director")

urlpatterns = router.urls
