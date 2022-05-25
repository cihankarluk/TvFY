from TvFY.core.helpers import read_file
from TvFY.genre.models import Genre


class GenreService:

    @classmethod
    def insert_genre_fixtures(cls):
        genre_data = read_file(path="fixtures/genres.json", is_json=True)

        genres = [Genre(name=item["fields"]["name"], detail=item["fields"]["detail"]) for item in genre_data]
        Genre.objects.bulk_create(genres)
