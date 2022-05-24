from TvFY.core.routers import RestRouter
from TvFY.country.views import CountryViewSet

router = RestRouter()

router.register("", CountryViewSet, basename="country")

urlpatterns = router.urls
