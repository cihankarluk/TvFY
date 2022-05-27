import datetime
import json
import os
from ctypes import Union
from typing import List, Any

from django.conf import settings
from django.test import TestCase
from model_bakery import baker
from rest_framework.test import APIClient

from TvFY.actor.models import Actor
from TvFY.country.models import Country
from TvFY.director.models import Director
from TvFY.genre.models import Genre
from TvFY.genre.service import GenreService
from TvFY.language.models import Language

__all__ = ["BaseTestCase"]

from TvFY.movies.models import Movie


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.now = datetime.datetime.now(tz=datetime.timezone.utc)
        GenreService.load_genres()

    @staticmethod
    def read_file(path, is_json=False):
        with open(os.path.join(settings.TEST_DATASET_DIR, path)) as f:
            file = f.read()
            if is_json:
                file = json.loads(file)
            return file

    @classmethod
    def is_subset(cls, attrs: set, results: Any) -> bool:
        if not isinstance(results, list):
            results: List[dict] = [results]

        is_subset: bool = all(
            attrs.issubset(transaction) and attrs.issuperset(transaction) for transaction in results
        )
        return is_subset

    # MODELS

    @classmethod
    def create_models(cls):
        cls.create_country()
        cls.create_language()
        cls.create_genre()
        cls.create_actor()
        cls.create_director()
        cls.create_movie()

    @classmethod
    def create_country(
            cls,
            count=10,
            name="test",
    ) -> List[Country]:
        countries = []
        for index in range(count):
            countries.append(baker.make(
                Country,
                name=f"{name}_{index}"
            ))
        return countries

    @classmethod
    def create_language(
            cls,
            count=10,
            name="test",
    ) -> List[Language]:
        languages = []
        for index in range(count):
            languages.append(baker.make(
                Language,
                name=f"{name}_{index}"
            ))
        return languages

    @classmethod
    def create_genre(
            cls,
            count=10,
            name="",
            detail="",
    ):
        genres = []
        for index in range(count):
            genres.append(baker.make(
                Genre,
                name=f"{name}_{index}",
                detail=f"{detail}_{index}",
            ))
        return genres

    @classmethod
    def create_actor(
            cls,
            index_start=0,
            count=10,
            tvfy_code="",
            first_name="",
            last_name="",
            full_name="",
            imdb_url="https://www.test.com/name/",
            born_date=None,
            born_at=None,
            died_date=None,
            died_at=None,
            perks=None,
            oscars=None,
            oscar_nominations=None,
            wins=None,
            nominations=None,
            is_updated=False,
    ) -> List[Actor]:
        actors = []
        for index in range(index_start, count+index_start, 1):
            actors.append(baker.make(
                Actor,
                tvfy_code=f"{tvfy_code}_{index}",
                first_name=f"{first_name}_{index}",
                last_name=f"{last_name}_{index}",
                full_name=f"{full_name}_{index}",
                imdb_url=f"{imdb_url}{index}/",
                born_date=born_date,
                born_at=born_at,
                died_date=died_date,
                died_at=died_at,
                perks=perks,
                oscars=oscars,
                oscar_nominations=oscar_nominations,
                wins=wins,
                nominations=nominations,
                is_updated=is_updated,
            ))
        return actors

    @classmethod
    def create_director(
            cls,
            index_start=0,
            count=10,
            tvfy_code="",
            first_name="",
            last_name="",
            full_name="",
            imdb_url="https://www.test.com/name/",
            rt_url="https://www.rt-test.com/name/",
            born_date=None,
            born_at=None,
            died_date=None,
            died_at=None,
            perks=None,
            oscars=None,
            oscar_nominations=None,
            wins=None,
            nominations=None,
            is_updated=False,
    ) -> List[Director]:
        directors = []
        for index in range(index_start, count + index_start, 1):
            directors.append(baker.make(
                Director,
                tvfy_code=f"{tvfy_code}_{index}",
                first_name=f"{first_name}_{index}",
                last_name=f"{last_name}_{index}",
                full_name=f"{full_name}_{index}",
                imdb_url=f"{imdb_url}{index}/",
                rt_url=f"{rt_url}{index}/",
                born_date=born_date,
                born_at=born_at,
                died_date=died_date,
                died_at=died_at,
                perks=perks,
                oscars=oscars,
                oscar_nominations=oscar_nominations,
                wins=wins,
                nominations=nominations,
                is_updated=is_updated,
            ))
        return directors

    @classmethod
    def create_movie(
            cls,
            index_start=0,
            count=10,
            tvfy_code="",
            title="",
            storyline=None,
            release_date=None,
            run_time=None,
            rt_tomatometer_rate=None,
            imdb_popularity=None,
            imdb_rate=None,
            imdb_vote_count=None,
            wins=None,
            nominations=None,
            budget=None,
            budget_currency=None,
            usa_opening_weekend=None,
            usa_opening_weekend_currency=None,
            ww_gross=None,
            imdb_url="https://test.com",
            rotten_tomatoes_url="https://rt-test.com",
    ) -> List[Movie]:
        movies = []
        for index in range(index_start, count + index_start, 1):
            movies.append(baker.make(
                Movie,
                tvfy_code=f"{tvfy_code}_{index}",
                title=f"{title}_{index}",
                storyline=storyline,
                release_date=release_date,
                run_time=run_time,
                rt_tomatometer_rate=rt_tomatometer_rate,
                imdb_popularity=imdb_popularity,
                imdb_rate=imdb_rate,
                imdb_vote_count=imdb_vote_count,
                wins=wins,
                nominations=nominations,
                budget=budget,
                budget_currency=budget_currency,
                usa_opening_weekend=usa_opening_weekend,
                usa_opening_weekend_currency=usa_opening_weekend_currency,
                ww_gross=ww_gross,
                imdb_url=f"{imdb_url}/{index}/",
                rotten_tomatoes_url=f"{rotten_tomatoes_url}/{index}",
            ))
        return movies
