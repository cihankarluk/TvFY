from django.urls import path

from TvFY.director import views

urlpatterns = [path("", views.DirectorView.as_view(), name="director")]
