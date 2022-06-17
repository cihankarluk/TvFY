import json
import os
import re
from datetime import datetime
from threading import local
from typing import Optional, Union
from uuid import uuid4

from django.core import validators
from django.utils.deconstruct import deconstructible

_threadlocals = local()


@deconstructible
class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r"^[\w.@+-]+$"
    message = "Enter a valid username. This value may contain only letters, " "numbers, and @/./+/-/_ characters."

    flags = 0


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


def regex_search(content: str, pattern: str) -> Optional[Union[str, int]]:
    try:
        if search_string := re.search(pattern, content):
            search_string = search_string.group()
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


def giveup_handler():
    raise KeyError
