from TvFY.actor.models import Actor
from TvFY.collector.imdb import IMDBScrapper
from TvFY.collector.tomatoes import TomatoesScrapper
from TvFY.core.models import Country, Language
from TvFY.director.models import Director
from TvFY.genre.models import Genre
from TvFY.movies.models import Movie, MovieCast


class MovieService:
    def __init__(self, search_data):
        self.search_data = search_data

    @property
    def get_genres(self):
        genres = set(self.search_data.get("rt_genre", {}))
        genres.update(set(self.search_data.get("imdb_genre", {})))
        genre_ids = Genre.objects.filter(name__in=genres).values_list("id", flat=True)
        return genre_ids

    @property
    def get_or_create_language(self):
        language_objs = []
        for language in self.search_data.get("language", []):
            language_obj, _ = Language.objects.get_or_create(language=language)
            language_objs.append(language_obj)
        return language_objs

    @property
    def get_or_create_country(self):
        country_objs = []
        for country in self.search_data.get("country", []):
            country_obj, _ = Country.objects.get_or_create(country=country)
            country_objs.append(country_obj)
        return country_objs

    @property
    def get_or_create_director(self):
        imdb_url = f'{IMDBScrapper.BASE_URL}{self.search_data["imdb_creator_url"]}'
        rt_url = f'{TomatoesScrapper.BASE_URL}{self.search_data["rt_creator_url"]}'
        director, _ = Director.objects.get_or_create(
            first_name=self.search_data["director"]["first_name"],
            last_name=self.search_data["director"]["last_name"],
            imdb_url=imdb_url,
            rt_url=rt_url,
        )
        return director

    def create_movie(self) -> Movie:
        movie_data = {
            "name": self.search_data["title"],
            "storyline": self.search_data.get("storyline"),
            "release_date": self.search_data.get("release_date"),
            "run_time": self.search_data.get("run_time"),
            "rt_tomatometer": self.search_data.get("rt_tomatometer"),
            "rt_tomatometer_count": self.search_data.get("rt_tomatometer_count"),
            "rt_audience_rate": self.search_data.get("rt_audience_rate"),
            "rt_audience_rate_count": self.search_data.get("rt_audience_rate_count"),
            "imdb_popularity": self.search_data.get("popularity"),
            "imdb_rate": self.search_data.get("total_imdb_rate"),
            "imdb_vote_count": self.search_data.get("total_imdb_vote_count"),
            "wins": self.search_data.get("wins"),
            "nominations": self.search_data.get("nominations"),
            "budget": self.search_data.get("budget"),
            "usa_opening_weekend": self.search_data.get("usa_opening_weekend"),
            "ww_gross": self.search_data.get("ww_gross"),
            "imdb_url": self.search_data.get("imdb_url"),
            "rotten_tomatoes_url": self.search_data.get("rotten_tomatoes_url"),
            "director": self.get_or_create_director,
        }

        movie = Movie.objects.create(**movie_data)

        for genre in self.get_genres:
            movie.genres.add(genre)
        for country in self.get_or_create_country:
            movie.country.add(country)
        for language in self.get_or_create_language:
            movie.language.add(language)

        return movie


class MovieCastService:
    def __init__(self, search_data: dict, movie: Movie):
        self.search_data = search_data
        self.movie = movie

    @staticmethod
    def get_or_create_actor(actor_data):
        actor, _ = Actor.objects.get_or_create(
            first_name=actor_data["first_name"], last_name=actor_data["last_name"]
        )
        return actor

    def create_movie_cast(self):
        movie_cast = []
        for cast in self.search_data.get("cast", []):
            actor = self.get_or_create_actor(cast)
            movie_cast.append(
                MovieCast(
                    character_name=cast["character_name"], movie=self.movie, actor=actor
                )
            )
        MovieCast.objects.bulk_create(movie_cast)
