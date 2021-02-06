from rest_framework.exceptions import ValidationError


class ValidationError(ValidationError):
    code = "VALIDATION_ERROR"


class UsernameAlreadyExists(ValidationError):
    code = "USERNAME_ALREADY_EXISTS"
