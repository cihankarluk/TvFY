from django.urls import path

from TvFY.series import views

urlpatterns = [
    path("", views.SeriesView.as_view(), name="series"),
    path("<str:tvfy_code>", views.SeriesDetailView.as_view(), name="series_detail"),
]
