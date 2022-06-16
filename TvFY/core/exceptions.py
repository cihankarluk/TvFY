from rest_framework.exceptions import ValidationError, NotFound


class ValidationError(ValidationError):
    code = "VALIDATION_ERROR"


class UsernameAlreadyExists(ValidationError):
    code = "USERNAME_ALREADY_EXISTS"


class SeriesDoesNotExist(ValidationError):
    code = "SERIES_DOES_NOT_EXISTS"


class SourceUrlNotFound(ValidationError):
    code = "SOURCE_URL_NOT_FOUND"


class NotAbleToFindDirectorSourceUrl(ValidationError):
    code = "DIRECTOR_SOURCE_URL_NOT_FOUND"


class MovieNotFoundError(NotFound):
    code = "MOVIE_NOT_FOUND"


class SeriesNotFoundError(NotFound):
    code = "SERIES_NOT_FOUND"


class ActorNotFoundError(NotFound):
    code = "ACTOR_NOT_FOUND"


class DirectorNotFoundError(NotFound):
    code = "DIRECTOR_NOT_FOUND"
