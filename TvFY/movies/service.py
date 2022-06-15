from typing import Optional

from TvFY.actor.service import ActorService
from TvFY.country.service import CountryService
from TvFY.director.service import DirectorService
from TvFY.genre.service import GenreService
from TvFY.language.service import LanguageService
from TvFY.movies.models import Movie, MovieCast


class MovieService:

    @classmethod
    def prepare_movie_data(cls, search_data: dict[str, ...]) -> dict[str, ...]:
        movie_data = {}

        if imdb_url := search_data.get("imdb_url"):
            movie_data.update(search_data[imdb_url])  # IMDB data for that movie
            movie_data.update(search_data[f"{imdb_url}fullcredits"])  # CAST
            movie_data["imdb_url"] = imdb_url
        if rt_url := search_data.get("rotten_tomatoes_url"):
            movie_data.update(search_data[rt_url])
            movie_data["rotten_tomatoes_url"] = rt_url

        return movie_data

    @classmethod
    def get_movie(cls, filter_map: dict[str, ...]) -> Optional[Movie]:
        movie = None
        movie_query = Movie.objects.filter(**filter_map)
        if movie_query.exists():
            movie = movie_query.get()

        return movie

    @classmethod
    def check_movie_exists(cls, movie_data: dict[str, ...]) -> Optional[Movie]:
        movie = None
        if imdb_url := movie_data.get("imdb_url"):
            movie = cls.get_movie(filter_map={"imdb_url": imdb_url})
        elif rotten_tomatoes_url := movie_data.get("rotten_tomatoes_url"):
            movie = cls.get_movie(filter_map={"rotten_tomatoes_url": rotten_tomatoes_url})

        return movie

    @classmethod
    def create_movie_model_data(cls, movie_data: dict[str, ...]) -> dict[str, ...]:
        """
        Prepare data for movie model.
        """
        movie_model_data = {
            "title": movie_data.get("imdb_title") or movie_data.get("rt_title"),
            "storyline": movie_data.get("rt_storyline"),
            "release_date": movie_data.get("release_date"),
            "run_time": movie_data.get("run_time"),
            "imdb_popularity": movie_data.get("imdb_popularity"),
            "imdb_rate": movie_data.get("imdb_rate"),
            "imdb_vote_count": movie_data.get("imdb_vote_count"),
            "wins": movie_data.get("wins"),
            "nominations": movie_data.get("nominations"),
            "oscar_wins": movie_data.get("oscar_wins"),
            "oscar_nominations": movie_data.get("oscar_nominations"),
            "budget_amount": movie_data.get("budget_amount"),
            "budget_currency": movie_data.get("budget_currency"),
            "usa_ow_amount": movie_data.get("usa_ow_amount"),
            "usa_ow_currency": movie_data.get("usa_ow_currency"),
            "ww_amount": movie_data.get("ww_amount"),
            "ww_currency": movie_data.get("ww_currency"),
            "metacritic_score": movie_data.get("metacritic_score"),
            "rt_tomatometer_rate": movie_data.get("rt_tomatometer_rate"),
            "rt_tomatometer_count": movie_data.get("rt_tomatometer_count"),
            "rt_audience_rate": movie_data.get("rt_audience_rate"),
            "rt_audience_count": movie_data.get("rt_audience_count"),
            "imdb_url": movie_data.get("imdb_url"),
            "rotten_tomatoes_url": movie_data.get("rotten_tomatoes_url"),
            "director": DirectorService.get_or_create_director(search_data=movie_data),
        }

        return movie_model_data

    @classmethod
    def update_movie(cls, movie: Movie, movie_data: dict[str, ...]) -> Movie:
        """
        Genre, Country, Language, Director fields are expected to not change.
        In that sense we only update movie model fields.
        """
        movie_model_data = cls.create_movie_model_data(movie_data=movie_data)
        for field, value in movie_model_data.items():
            setattr(movie, field, value)
        movie.save()

        return movie

    @classmethod
    def create_movie(cls, movie_data: dict[str, ...]) -> Movie:
        """
        Create movie and casts with them.
        """
        movie_model_data = cls.create_movie_model_data(movie_data=movie_data)
        movie = Movie.objects.create(**movie_model_data)
        for genre in GenreService.get_genre_ids(search_data=movie_data):
            movie.genres.add(genre)
        for country in CountryService.get_or_create_multiple_country(search_data=movie_data):
            movie.country.add(country)
        for language in LanguageService.get_or_create_multiple_language(search_data=movie_data):
            movie.language.add(language)
        MovieCastService.bulk_create_movie_cast(movie=movie, movie_data=movie_data)

        return movie

    @classmethod
    def create_or_update_movie(cls, search_data: dict[str, ...]) -> Movie:
        movie_data = cls.prepare_movie_data(search_data=search_data)

        if movie := cls.check_movie_exists(movie_data=movie_data):
            movie = cls.update_movie(movie=movie, movie_data=movie_data)
        else:
            movie = cls.create_movie(movie_data=movie_data)

        return movie


class MovieCastService:

    @classmethod
    def bulk_create_movie_cast(cls, movie: Movie, movie_data: dict[str, ...]):
        """
        This method creates Actor in same time if the actor is not registered to db.
        """
        cast_data = movie_data.get("cast", [])
        actor_dict = ActorService.create_multiple_actor(cast_data=cast_data)

        movie_cast = []
        for cast in cast_data:
            movie_cast.append(
                MovieCast(
                    character_name=cast["character_name"],
                    movie=movie,
                    actor=actor_dict[cast["imdb_actor_url"]]["actor"],
                )
            )
        MovieCast.objects.bulk_create(movie_cast)
