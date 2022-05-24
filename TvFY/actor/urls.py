from TvFY.actor.views import ActorViewSet
from TvFY.core.routers import RestRouter

router = RestRouter()

router.register("", ActorViewSet, basename="actor")

urlpatterns = router.urls
