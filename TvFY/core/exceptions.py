from rest_framework.exceptions import ValidationError


class ValidationError(ValidationError):
    code = "VALIDATION_ERROR"


class UsernameAlreadyExists(ValidationError):
    code = "USERNAME_ALREADY_EXISTS"


class SeriesDoesNotExist(ValidationError):
    code = "SERIES_DOES_NOT_EXISTS"


class NotAbleToFindMovieSourceUrl(ValidationError):
    code = "MOVIE_SOURCE_URL_NOT_FOUND"


class NotAbleToFindDirectorSourceUrl(ValidationError):
    code = "DIRECTOR_SOURCE_URL_NOT_FOUND"
