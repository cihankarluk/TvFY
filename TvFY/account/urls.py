from django.urls import path

from TvFY.account import views

urlpatterns = [
    path('signup', views.UserSignUp.as_view(), name='sing_up'),
    path('signin', views.UserSingIn.as_view(), name='sing_in'),
]
