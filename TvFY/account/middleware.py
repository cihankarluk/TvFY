import base64

from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from rest_framework import status

from TvFY.account.models import Account

EXEMPT_URLS = settings.EXEMPT_URLS


class AccountAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    @staticmethod
    def exempt_url_check(path):
        """Control over url if it accessible for everyone."""
        permission = [path.startswith(reverse(url_)) for url_ in EXEMPT_URLS]
        return any(permission)

    @staticmethod
    def display_error_message(status_code, code, error_message):
        data = {
            "status_code": status_code,
            "code": code,
            "error_message": error_message,
        }
        return JsonResponse(data, status=status_code)

    def process_view(self, request, view_func, view_args, view_kwargs):
        auth = request.META.get("HTTP_AUTHORIZATION", "").split()
        content_type = request.META.get("CONTENT_TYPE")
        request_method = request.META.get("REQUEST_METHOD")
        path = request.path

        if self.exempt_url_check(path):
            # If the endpoint does not require authentication
            return

        if not auth or auth[0].lower() != "basic":
            return self.display_error_message(
                status_code=status.HTTP_401_UNAUTHORIZED,
                code="WRONG_AUTH_TYPE",
                error_message="Authentication type must be Basic Authentication",
            )

        try:
            auth_decoded = base64.b64decode(auth[1]).decode("utf-8")
            auth_parts = auth_decoded.partition(":")
        except TypeError:
            return self.display_error_message(
                status_code=status.HTTP_401_UNAUTHORIZED,
                code="WRONG_AUTH_TYPE",
                error_message="Authentication type must be Basic Authentication",
            )

        username, password = auth_parts[0], auth_parts[2]
        try:
            account = Account.objects.get(username=username)
        except Account.DoesNotExist:
            return self.display_error_message(
                status_code=status.HTTP_401_UNAUTHORIZED,
                code="WRONG_USERNAME_OR_PASSWORD",
                error_message="Entered username or password is wrong.",
            )

        if not account.check_password(password):
            return self.display_error_message(
                status_code=status.HTTP_401_UNAUTHORIZED,
                code="WRONG_USERNAME_OR_PASSWORD",
                error_message="Entered username or password is wrong.",
            )

        post_conditions = all(
            [
                request_method == "POST",
                content_type != "application/json",
                content_type != "application/x-www-form-urlencoded",
            ]
        )  # admin side

        if post_conditions:
            return self.display_error_message(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                code="WRONG_MEDIA_TYPE",
                error_message="Media type is wrong.",
            )

        setattr(request, "account", account)
