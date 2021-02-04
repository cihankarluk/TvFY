from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status


class UserAuthenticationMiddleware(MiddlewareMixin):
    @staticmethod
    def display_error_message(msg=None, **kwargs):
        data = {
            "status_code": status.HTTP_401_UNAUTHORIZED,
            "code": "AUTHENTICATION_FAIL",
            "error_message": msg,
        }
        return JsonResponse(data, status=401)

    def process_view(self, request, view_func, view_args, view_kwargs):
        username = request.META.get("HTTP_TOKEN")
        content_type = request.META.get("CONTENT_TYPE")
        request_method = request.META.get("REQUEST_METHOD")

        post_conditions = all(
            [
                request_method == "POST",
                content_type != "application/json",
                content_type != "application/x-www-form-urlencoded",
            ]
        )  # admin side
