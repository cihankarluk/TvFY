from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r'^[\w.@+-]+$'
    message = ("Enter a valid username. This value may contain only letters, "
               "numbers, and @/./+/-/_ characters.")

    flags = 0
