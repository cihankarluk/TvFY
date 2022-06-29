import datetime
import json
import os
from typing import Any
from uuid import uuid4

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from model_bakery import baker
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from TvFY.actor.models import Actor
from TvFY.country.models import Country
from TvFY.director.models import Director
from TvFY.genre.models import Genre
from TvFY.genre.service import GenreService
from TvFY.language.models import Language

__all__ = ["BaseTestCase"]

from TvFY.movies.models import Movie
from TvFY.series.models import Episode, Season, Series, SeriesCast
from TvFY.user.models import UserMovies, UserSeries

UserModel = get_user_model()


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.uid = self.get_random_str()
        self.account = UserModel.objects.create_user(
            username=self.uid,
            first_name=f"first_name_{self.uid}",
            last_name=f"last_name_{self.uid}",
            email=f"{self.uid}@tvfy.com",
            password=self.uid,
            is_superuser=False,
            is_staff=False,
        )
        self.authenticate_client(self.client)
        self.now = datetime.datetime.now(tz=datetime.timezone.utc)
        GenreService.load_genres()

    @classmethod
    def get_random_str(cls) -> str:
        return str(uuid4())[:10]

    def authenticate_client(self, client):
        login_url = reverse("rest_login")
        login_request_data = {
            "username": self.account.username,
            "password": self.account.username,
        }
        response = self.client.post(login_url, data=login_request_data)
        token = response.data["access_token"]
        client.credentials(HTTP_AUTHORIZATION=f"JWT {token}")

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
            results: list[dict] = [results]

        is_subset: bool = all(attrs.issubset(transaction) and attrs.issuperset(transaction) for transaction in results)
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
    ) -> list[Country]:
        countries = []
        for index in range(count):
            countries.append(baker.make(Country, name=f"{name}_{index}"))
        return countries

    @classmethod
    def create_language(
        cls,
        count=10,
        name="test",
    ) -> list[Language]:
        languages = []
        for index in range(count):
            languages.append(baker.make(Language, name=f"{name}_{index}"))
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
            genres.append(
                baker.make(
                    Genre,
                    name=f"{name}_{index}",
                    detail=f"{detail}_{index}",
                )
            )
        return genres

    @classmethod
    def create_actor(
        cls,
        index_start=0,
        count=10,
        tvfy_code=None,
        first_name=None,
        last_name=None,
        full_name=None,
        imdb_url=None,
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
    ) -> list[Actor]:
        actors = []
        for index in range(index_start, count + index_start, 1):
            actors.append(
                baker.make(
                    Actor,
                    tvfy_code=tvfy_code or f"{tvfy_code}_{index}",
                    first_name=first_name or f"{first_name}_{index}",
                    last_name=last_name or f"{last_name}_{index}",
                    full_name=full_name or f"{full_name}_{index}",
                    imdb_url=imdb_url or f"{imdb_url}{index}/",
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
                )
            )
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
    ) -> list[Director]:
        directors = []
        for index in range(index_start, count + index_start, 1):
            directors.append(
                baker.make(
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
                )
            )
        return directors

    @classmethod
    def create_movie(
        cls,
        index_start=0,
        count=10,
        title="",
        storyline=None,
        release_date=None,
        run_time=None,
        rt_tomatometer_rate=None,
        rt_audience_rate=None,
        imdb_popularity=None,
        imdb_rate=None,
        imdb_vote_count=None,
        wins=None,
        nominations=None,
        oscar_wins=None,
        oscar_nominations=None,
        budget_amount=None,
        budget_currency=None,
        usa_ow_amount=None,
        usa_ow_currency=None,
        ww_amount=None,
        ww_currency=None,
        metacritic_score=None,
        imdb_url="https://test.com",
        rotten_tomatoes_url="https://rt-test.com",
    ) -> list[Movie]:
        movies = []
        for index in range(index_start, count + index_start, 1):
            movies.append(
                baker.make(
                    Movie,
                    title=f"{title}_{index}",
                    storyline=storyline,
                    release_date=release_date,
                    run_time=run_time,
                    rt_tomatometer_rate=rt_tomatometer_rate,
                    rt_audience_rate=rt_audience_rate,
                    imdb_popularity=imdb_popularity,
                    imdb_rate=imdb_rate,
                    imdb_vote_count=imdb_vote_count,
                    wins=wins,
                    nominations=nominations,
                    oscar_wins=oscar_wins,
                    oscar_nominations=oscar_nominations,
                    budget_amount=budget_amount,
                    budget_currency=budget_currency,
                    usa_ow_amount=usa_ow_amount,
                    usa_ow_currency=usa_ow_currency,
                    ww_amount=ww_amount,
                    ww_currency=ww_currency,
                    metacritic_score=metacritic_score,
                    imdb_url=f"{imdb_url}/{index}/",
                    rotten_tomatoes_url=f"{rotten_tomatoes_url}/{index}",
                )
            )
        return movies

    @classmethod
    def create_series(
        cls,
        index_start=0,
        count=10,
        title=None,
        storyline=None,
        release_date=None,
        end_date=None,
        run_time=None,
        is_active=None,
        season_count=None,
        wins=None,
        nominations=None,
        oscar_wins=None,
        oscar_nominations=None,
        tv_network=None,
        imdb_rate=None,
        imdb_vote_count=None,
        imdb_popularity=None,
        imdb_url=None,
        rt_tomatometer_rate=None,
        rt_audience_rate=None,
        rotten_tomatoes_url=None,
        metacritic_score=None,
        creator=None,
    ) -> list[Series]:
        series = []
        for index in range(index_start, count + index_start, 1):
            series.append(
                baker.make(
                    Series,
                    title=title or f"{title}_{index}",
                    storyline=storyline,
                    release_date=release_date,
                    end_date=end_date,
                    run_time=run_time,
                    is_active=is_active,
                    season_count=season_count,
                    wins=wins,
                    nominations=nominations,
                    oscar_wins=oscar_wins,
                    oscar_nominations=oscar_nominations,
                    tv_network=tv_network,
                    imdb_rate=imdb_rate,
                    imdb_vote_count=imdb_vote_count,
                    imdb_popularity=imdb_popularity,
                    imdb_url=imdb_url or f"{imdb_url}/{index}/",
                    rt_tomatometer_rate=rt_tomatometer_rate,
                    rt_audience_rate=rt_audience_rate,
                    rotten_tomatoes_url=rotten_tomatoes_url or f"{rotten_tomatoes_url}/{index}",
                    metacritic_score=metacritic_score,
                    creator=creator,
                )
            )
        return series

    @classmethod
    def create_series_cast(
        cls,
        index_start=0,
        count=10,
        character_name="",
        episode_count=None,
        start_acting=None,
        end_acting=None,
        series=None,
        actor=None,
    ) -> list[SeriesCast]:
        series_cast = []
        for index in range(index_start, count + index_start, 1):
            series_cast.append(
                baker.make(
                    SeriesCast,
                    character_name=character_name or f"{character_name}_{index}",
                    episode_count=episode_count or index,
                    start_acting=start_acting,
                    end_acting=end_acting,
                    series=series or cls.create_series(index_start=index_start + index, count=1)[0],
                    actor=actor or cls.create_actor(index_start=index_start + index, count=1)[0],
                )
            )
        return series_cast

    @classmethod
    def create_season(
        cls,
        index_start=0,
        count=10,
        season=None,
        imdb_url=None,
        series=None,
    ) -> list[Season]:
        seasons = []
        for index in range(index_start, count + index_start, 1):
            seasons.append(
                baker.make(
                    Season,
                    season=season or f"{index}",
                    imdb_url=imdb_url or f"{imdb_url}/{index}/",
                    series=series or cls.create_series(index_start=index_start + index, count=1)[0],
                )
            )
        return seasons

    @classmethod
    def create_episode(
        cls,
        index_start=0,
        count=10,
        title=None,
        storyline=None,
        release_date=None,
        imdb_rate=None,
        imdb_vote_count=None,
        episode=None,
        season=None,
    ) -> list[Episode]:
        episodes = []
        for index in range(index_start, count + index_start, 1):
            episodes.append(
                baker.make(
                    Episode,
                    title=title or f"{title}_{index}",
                    storyline=storyline,
                    release_date=release_date,
                    imdb_rate=imdb_rate,
                    imdb_vote_count=imdb_vote_count,
                    episode=episode,
                    season=season or cls.create_season(index_start=index_start + index, count=1)[0],
                )
            )
        return episodes

    def create_user_movies(
        self,
        index_start=0,
        count=10,
        user=None,
        movie=None,
        is_watched=True,
        is_going_to_watch=False,
    ) -> list[UserMovies]:
        user_movies = []
        for index in range(index_start, count + index_start, 1):
            user_movies.append(
                baker.make(
                    UserMovies,
                    user=user or self.account,
                    movie=movie or self.create_movie(index_start=index_start + index, count=1)[0],
                    is_watched=is_watched,
                    is_going_to_watch=is_going_to_watch,
                )
            )
        return user_movies

    def create_user_series(
        self,
        index_start=0,
        count=10,
        user=None,
        series=None,
        watched_season=None,
        last_watched_episode=None,
        is_watched=True,
        is_going_to_watch=False,
    ) -> list[UserSeries]:
        user_series = []
        for index in range(index_start, count + index_start, 1):
            user_series.append(
                baker.make(
                    UserSeries,
                    user=user or self.account,
                    series=series or self.create_series(index_start=index_start + index, count=1)[0],
                    watched_season=watched_season or self.create_season(index_start=index_start + index, count=1)[0],
                    last_watched_episode=last_watched_episode,
                    is_watched=is_watched,
                    is_going_to_watch=is_going_to_watch,
                )
            )
        return user_series
