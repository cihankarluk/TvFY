import json
import os
import random
import string
from datetime import datetime
from unittest.mock import Mock

import bs4
from django.core import validators
from django.utils.deconstruct import deconstructible
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler


@deconstructible
class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r'^[\w.@+-]+$'
    message = ("Enter a valid username. This value may contain only letters, "
               "numbers, and @/./+/-/_ characters.")

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

    code = getattr(exc, 'code', None)
    if code is None:
        code = 'VALIDATION_ERROR'

    if not isinstance(error_message, dict):
        try:
            error_message = json.loads(error_message)
        except ValueError:
            pass

    data = {
        'status_code': response.status_code,
        'code': code,
        'error_message': error_message
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
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for _ in range(length))
    return result_str


def read_file(path, is_json=False):
    root = os.getcwd()
    with open(os.path.join(root, path)) as f:
        file = f.read()
        if is_json:
            file = json.loads(file)
        return file
