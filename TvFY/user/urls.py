from django.urls import path, re_path

from TvFY.core.routers import RestRouter
from TvFY.user.views import (
    UserLoginView,
    UserLogoutView,
    UserPasswordChangeView,
    UserPasswordResetConfirmView,
    UserPasswordResetView,
    UserResendEmailVerificationView,
    UserSignupView,
    UserVerifyEmailView,
    UserViewSet,
)

router = RestRouter()

router.register("", UserViewSet, basename="user")

urlpatterns = router.urls

urlpatterns += [
    path("signup/", UserSignupView.as_view(), name="rest_register"),
    path("login/", UserLoginView.as_view(), name="rest_login"),
    path("logout/", UserLogoutView.as_view(), name="rest_logout"),
    path(
        "password/reset/",
        UserPasswordResetView.as_view(),
        name="rest_password_reset",
    ),
    path(
        "password/reset/confirm/<uidb64>/<token>/",
        UserPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password/change/",
        UserPasswordChangeView.as_view(),
        name="rest_password_change",
    ),
    path(
        "resend-email/",
        UserResendEmailVerificationView.as_view(),
        name="rest_resend_email",
    ),
    re_path(
        r"^verify-email/(?P<key>[-:\w]+)/$",
        UserVerifyEmailView.as_view(),
        name="account_confirm_email",
    ),
    # path('email-verification-sent/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
]
