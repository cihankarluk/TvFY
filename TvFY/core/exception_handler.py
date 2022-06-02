import logging

from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import set_rollback


logger = logging.getLogger(__name__)


def exception_handler(exc, context):
    """Returns the response that should be used for any given exception.

    By default, we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        status_code = exc.status_code
        data = {
            "code": status_code,
            "type": exc.__class__.__name__,
            "reason": exc.detail
        }
    else:
        status_code = 500
        data = {
            "code": -1,
            "type": "UnexpectedException",
            "reason": "An unexpected error has occurred."
        }

        # this line is a MUST for mail_admins handler to catch errors and send mail
        logger.exception(exc)

    set_rollback()
    return Response(data, status=status_code)
