import json
import os
import re
from datetime import datetime
from threading import local
from unittest.mock import Mock
from uuid import uuid4

import bs4
from django.core import validators
from django.utils.deconstruct import deconstructible
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler

_threadlocals = local()


@deconstructible
class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r"^[\w.@+-]+$"
    message = (
        "Enter a valid username. This value may contain only letters, "
        "numbers, and @/./+/-/_ characters."
    )

    flags = 0


def custom_exception_handler(exc, context: dict):
    """
    Rest Framework exception handler
    :param exc: AttributeError etc
    :param context: dict
    :return: raise exc
    """
    response = exception_handler(exc, context)
    if not isinstance(exc, APIException):
        raise exc
    elif isinstance(response.data, list):
        error_message = response.data[0]
    elif isinstance(response.data, dict):
        error_message = response.data

    code = getattr(exc, "code", None)
    if code is None:
        code = "VALIDATION_ERROR"

    if not isinstance(error_message, dict):
        try:
            error_message = json.loads(error_message)
        except ValueError:
            pass

    data = {
        "status_code": response.status_code,
        "code": code,
        "error_message": error_message,
    }

    return Response(data, status=response.status_code, headers=response._headers)


def error_handler(func):
    def inner(self, soup: bs4, method: str, tag: str = None, **kwargs):
        result = func(self, soup, method, tag, **kwargs)
        if not result:
            mock = Mock()
            mock.return_value = []
            mock.text = ""
            mock.a.text = ""
            mock.find_all = []
            mock.find.text = ""
            return mock
        return result

    return inner


def get_date_time(date: str, pattern: str) -> datetime:
    return datetime.strptime(date, pattern)


def get_random_string(length):
    return str(uuid4())[:length]


def read_file(path, is_json=False):
    root = os.getcwd()
    with open(os.path.join(root, path)) as f:
        file = f.read()
        if is_json:
            file = json.loads(file)
        return file


def regex_search(content: str, pattern: str) -> str:
    try:
        search_string = re.search(pattern, content).group()
    except AttributeError:
        search_string = None
    return search_string


def get_thread_variable(key, default=None):
    return getattr(_threadlocals, key, default)


def get_current_request():
    return get_thread_variable("request", None)


def get_current_user():
    request = get_current_request()
    return getattr(request, "user", None) if request else None
