from django.db.models import QuerySet

from TvFY.core.helpers import read_file
from TvFY.genre.models import Genre


class GenreService:

    @classmethod
    def load_genres(cls):
        genre_data = read_file(path="fixtures/genres.json", is_json=True)

        genres = [Genre(name=item["fields"]["name"], detail=item["fields"]["detail"]) for item in genre_data]
        Genre.objects.bulk_create(genres)

    @classmethod
    def get_genre_ids(cls, search_data: dict[str, ...]) -> QuerySet:
        genres = set()
        for key, value in search_data.items():
            if "genre" in key:
                genres.update(set(value))
        genre_ids = Genre.objects.filter(name__in=genres).values_list("id", flat=True)

        return genre_ids
