from typing import Optional

from TvFY.actor.service import ActorService
from TvFY.core.exceptions import NotAbleToFindMovieSourceUrl
from TvFY.country.service import CountryService
from TvFY.director.service import DirectorService
from TvFY.genre.service import GenreService
from TvFY.language.service import LanguageService
from TvFY.movies.models import Movie, MovieCast


class MovieService:

    @classmethod
    def check_source_urls(cls, search_data: dict) -> None:
        """
        At least one of them concur to find data about that movie.
        """
        if not (search_data.get("imdb_url") or search_data.get("rotten_tomatoes_url")):
            raise NotAbleToFindMovieSourceUrl("Cannot find source url for that movie. If you know address please contact.")
        return None

    @classmethod
    def get_movie(cls, filter_map: dict) -> Optional[Movie]:
        movie_query = Movie.objects.filter(**filter_map)
        if movie_query.exists():
            movie = movie_query.get()
        else:
            movie = None
        return movie

    @classmethod
    def check_movie_exists(cls, search_data: dict) -> Optional[Movie]:
        if imdb_url := search_data.get("imdb_url"):
            movie = cls.get_movie(filter_map={"imdb_url": imdb_url})
        elif rotten_tomatoes_url := search_data.get("rotten_tomatoes_url"):
            movie = cls.get_movie(filter_map={"rotten_tomatoes_url": rotten_tomatoes_url})
        else:
            movie = None
        return movie

    @classmethod
    def create_movie(cls, movie_data: dict, search_data: dict) -> Movie:
        """
        Create movie and casts with them.
        """
        movie = Movie.objects.create(**movie_data)
        for genre in GenreService.get_genre_ids(search_data=search_data):
            movie.genres.add(genre)
        for country in CountryService.get_or_create_multiple_country(search_data=search_data):
            movie.country.add(country)
        for language in LanguageService.get_or_create_multiple_language(search_data=search_data):
            movie.language.add(language)
        MovieCastService.bulk_create_movie_cast(search_data=search_data, movie=movie)

        return movie

    @classmethod
    def update_movie(cls, movie: Movie, movie_data: dict) -> Movie:
        """
        Genre, Country, Language, Director fields are expected to not change.
        In that sense we only update movie fields.
        """
        for field, value in movie_data.items():
            setattr(movie, field, value)
        movie.save()
        return movie

    @classmethod
    def create_or_update_movie(cls, search_data: dict) -> Movie:
        cls.check_source_urls(search_data=search_data)

        movie_data = {
            "title": search_data["title"],
            "storyline": search_data.get("storyline"),
            "release_date": search_data.get("release_date"),
            "run_time": search_data.get("run_time"),
            "rt_tomatometer_rate": search_data.get("rt_tomatometer_rate"),
            "rt_audience_rate": search_data.get("rt_audience_rate"),
            "imdb_popularity": search_data.get("imdb_popularity"),
            "imdb_rate": search_data.get("imdb_rate"),
            "imdb_vote_count": search_data.get("imdb_vote_count"),
            "wins": search_data.get("wins"),
            "nominations": search_data.get("nominations"),
            "budget": search_data.get("budget"),
            "budget_currency": search_data.get("budget_currency"),
            "usa_opening_weekend": search_data.get("usa_opening_weekend"),
            "usa_opening_weekend_currency": search_data.get("usa_opening_weekend_currency"),
            "ww_gross": search_data.get("ww_gross"),
            "imdb_url": search_data.get("imdb_url"),
            "rotten_tomatoes_url": search_data.get("rotten_tomatoes_url"),
            "director": DirectorService.get_or_create_director(search_data=search_data),
        }

        if movie := cls.check_movie_exists(search_data=search_data):
            movie = cls.update_movie(movie=movie, movie_data=movie_data)
        else:
            movie = cls.create_movie(movie_data=movie_data, search_data=search_data)

        return movie


class MovieCastService:

    @classmethod
    def bulk_create_movie_cast(cls, search_data: dict, movie: Movie):
        """
        This method creates Actor in same time if the actor is not registered to db.
        """
        cast_data = search_data.get("cast", [])
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
