from dj_rest_auth.registration.views import RegisterView, VerifyEmailView, ResendEmailVerificationView
from dj_rest_auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.urls import path, re_path

from TvFY.core.routers import RestRouter
from TvFY.user.views import UserLogoutView

router = RestRouter()


urlpatterns = router.urls

urlpatterns += [
    path('signup/', RegisterView.as_view(), name='rest_register'),
    path('login/', LoginView.as_view(), name='rest_login'),
    path('logout/', UserLogoutView.as_view(), name='rest_logout'),
    path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
    path('resend-email/', ResendEmailVerificationView.as_view(), name="rest_resend_email"),
    re_path(r'^confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(), name='account_confirm_email'),
    path('email-verification-sent/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
]
