from TvFY.actor.models import Actor
from TvFY.core.models import Country, Language
from TvFY.director.models import Director
from TvFY.genre.models import Genre
from TvFY.movies.models import Movie, MovieCast


class MovieCastService:
    @staticmethod
    def get_or_create_actor(actor_data) -> Actor:
        actor, _ = Actor.objects.get_or_create(
            first_name=actor_data["first_name"],
            last_name=actor_data["last_name"],
            imdb_url=actor_data["imdb_actor_url"],
        )
        return actor

    @classmethod
    def create_movie_cast(cls, search_data: dict, movie: Movie):
        movie_cast = []
        for cast in search_data.get("cast", []):
            actor = cls.get_or_create_actor(cast)
            movie_cast.append(
                MovieCast(character_name=cast["character_name"], movie=movie, actor=actor)
            )
        MovieCast.objects.bulk_create(movie_cast)


class MovieService:
    def __init__(self, search_data):
        self.search_data = search_data

    @property
    def get_genres(self) -> list:
        genres = set(self.search_data.get("rt_genre", {}))
        genres.update(set(self.search_data.get("imdb_genre", {})))
        genre_ids = Genre.objects.filter(name__in=genres).values_list("id", flat=True)
        return genre_ids

    @property
    def get_or_create_language(self) -> list:
        language_objs = []
        for language in self.search_data.get("language", []):
            language_obj, _ = Language.objects.get_or_create(language=language)
            language_objs.append(language_obj)
        return language_objs

    @property
    def get_or_create_country(self) -> list:
        country_objs = []
        for country in self.search_data.get("country", []):
            country_obj, _ = Country.objects.get_or_create(country=country)
            country_objs.append(country_obj)
        return country_objs

    @property
    def get_or_create_director(self) -> Director:
        director, _ = Director.objects.get_or_create(
            first_name=self.search_data["rt_director"]["first_name"],
            last_name=self.search_data["rt_director"]["last_name"],
            imdb_director_url=self.search_data["imdb_director_url"],
            rt_director_url=self.search_data["rt_director_url"],
        )
        return director

    def create_movie(self) -> Movie:
        movie_data = {
            "title": self.search_data["title"],
            "storyline": self.search_data.get("storyline"),
            "release_date": self.search_data.get("release_date"),
            "run_time": self.search_data.get("run_time"),
            "rt_tomatometer_rate": self.search_data.get("rt_tomatometer_rate"),
            "rt_audience_rate": self.search_data.get("rt_audience_rate"),
            "imdb_popularity": self.search_data.get("imdb_popularity"),
            "imdb_rate": self.search_data.get("imdb_rate"),
            "imdb_vote_count": self.search_data.get("imdb_vote_count"),
            "wins": self.search_data.get("wins"),
            "nominations": self.search_data.get("nominations"),
            "budget": self.search_data.get("budget"),
            "budget_currency": self.search_data.get("budget_currency"),
            "usa_opening_weekend": self.search_data.get("usa_opening_weekend"),
            "usa_opening_weekend_currency": self.search_data.get(
                "usa_opening_weekend_currency"
            ),
            "ww_gross": self.search_data.get("ww_gross"),
            "imdb_url": self.search_data.get("imdb_url"),
            "rotten_tomatoes_url": self.search_data.get("rotten_tomatoes_url"),
            "director": self.get_or_create_director,
        }

        movie = Movie.objects.create(**movie_data)

        MovieCastService.create_movie_cast(search_data=self.search_data, movie=movie)

        for genre in self.get_genres:
            movie.genres.add(genre)
        for country in self.get_or_create_country:
            movie.country.add(country)
        for language in self.get_or_create_language:
            movie.language.add(language)

        return movie
