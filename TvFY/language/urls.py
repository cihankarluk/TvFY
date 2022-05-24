from TvFY.core.routers import RestRouter
from TvFY.language.views import LanguageViewSet

router = RestRouter()

router.register("", LanguageViewSet, basename="language")

urlpatterns = router.urls
