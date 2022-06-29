from allauth.account.auth_backends import AuthenticationBackend as AllauthAuthenticationBackend
from dj_rest_auth.jwt_auth import JWTCookieAuthentication
from django.contrib.auth import get_user_model
from rest_framework import exceptions


UserModel = get_user_model()


class AllowOnlyCustomerAllauthAuthenticationBackend(AllauthAuthenticationBackend):
    def authenticate(self, request, **credentials):
        return super().authenticate(request, **credentials)


class AllowOnlyCustomerJWTCookieAuthenticationBackend(JWTCookieAuthentication):
    def authenticate(self, request):
        authenticate_ = super().authenticate(request)
        if authenticate_ is not None:
            user, _ = authenticate_
            request.user = user
            return authenticate_
