from django.urls import path

from TvFY.actor import views

urlpatterns = [path("", views.ActorView.as_view(), name="actor")]
