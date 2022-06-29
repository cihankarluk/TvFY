from itests.base import BaseTestCase
from TvFY.collector.base import Scraper
from TvFY.movies.models import Movie
from TvFY.series.models import Series


class IMDBEpisodesTestCase(BaseTestCase):
    def setUp(self) -> None:
        self.expected_attrs = {
            "title",
            "storyline",
            "imdb_rate",
            "imdb_vote_count",
            "episode",
            "release_date",
            "imdb_url",
        }

    def test__1(self):
        urls = [
            "https://www.imdb.com/title/tt2098220/episodes?season=1",
        ]

        result = Scraper(urls=urls).handle()

        for url in urls:
            self.assertListEqual(
                [],
                self.take_diff(attrs=self.expected_attrs, results=result[url]["1"]),
            )

        episode_data = result[urls[0]]["1"][0]
        self.assertTrue(episode_data["title"])
        self.assertTrue(len(episode_data["storyline"]))
        self.assertTrue(episode_data["imdb_rate"])
        self.assertTrue(episode_data["imdb_vote_count"])
        self.assertTrue(episode_data["episode"])
        self.assertTrue(episode_data["release_date"])

    def test__2(self):
        # This case is for season entered to imdb however no episodes are released yet.
        url = "https://www.imdb.com/title/tt1190634/episodes?season=3"

        result = Scraper(urls=[url]).handle()

        self.assertListEqual(
            [],
            self.take_diff(attrs=self.expected_attrs, results=result[url]["3"]),
        )


class IMDBCastTestCase(BaseTestCase):
    def test__1(self):
        # Series Case
        expected_attrs = {
            "first_name",
            "last_name",
            "character_name",
            "episode_count",
            "start_acting",
            "end_acting",
            "imdb_actor_url",
        }
        url = "https://www.imdb.com/title/tt0182576/fullcredits"

        result = Scraper(urls=[url]).handle()

        self.assertListEqual(
            [],
            self.take_diff(attrs=expected_attrs, results=result[url]["cast"]),
        )

    def test__2(self):
        expected_attrs = {
            "first_name",
            "last_name",
            "character_name",
            "imdb_actor_url",
        }
        url = "https://www.imdb.com/title/tt0167260/fullcredits"

        result = Scraper(urls=[url], search_type=Movie.TYPE).handle()

        self.assertListEqual(
            [],
            self.take_diff(attrs=expected_attrs, results=result[url]["cast"]),
        )


class IMDBAwardsTestCase(BaseTestCase):
    def setUp(self) -> None:
        self.expected_attrs = {
            "wins",
            "nominations",
        }

    def test__1(self):
        url = "https://www.imdb.com/title/tt1190634/awards/"

        result = Scraper(urls=[url]).handle()

        self.assertListEqual([], self.take_diff(attrs=self.expected_attrs, results=result))

    def test__2(self):
        url = "https://www.imdb.com/title/tt2098220/awards/"

        result = Scraper(urls=[url]).handle()

        self.assertListEqual([], self.take_diff(attrs=self.expected_attrs, results=result))


class IMDBPersonalDataTestCase(BaseTestCase):
    def test__1(self):
        expected_attrs = {
            "born_date",
            "born_at",
            "died_date",
            "died_at",
            "oscar_nominations",
            "wins",
            "nominations",
            "perks",
        }
        url = "https://www.imdb.com/name/nm0000033/"

        results = Scraper(urls=[url]).handle()

        self.assertListEqual([], self.take_diff(attrs=expected_attrs, results=results[url]))

    def test__2(self):
        expected_attrs = {
            "born_date",
            "born_at",
            "perks",
        }
        url = "https://www.imdb.com/name/nm0391866/"

        results = Scraper(urls=[url]).handle()

        self.assertListEqual([], self.take_diff(attrs=expected_attrs, results=results[url]))

    def test__3(self):
        expected_attrs = {
            "wins",
            "nominations",
            "perks",
        }
        url = "https://www.imdb.com/name/nm0458647"

        results = Scraper(urls=[url]).handle()

        self.assertListEqual([], self.take_diff(attrs=expected_attrs, results=results[url]))


class IMDBHomePageTestCase(BaseTestCase):
    def test__movie1(self):
        expected_attrs = {
            "imdb_genre",
            "imdb_director",
            "imdb_director_url",
            "run_time",
            "imdb_popularity",
            "country",
            "language",
            "release_date",
            "imdb_title",
            "budget_amount",
            "budget_currency",
            "usa_ow_amount",
            "usa_ow_currency",
            "ww_amount",
            "ww_currency",
            "metacritic_score",
            "imdb_vote_count",
            "imdb_rate",
            "usa_ow_amount",
            "metacritic_score",
            "imdb_popularity",
            "usa_ow_currency",
            "wins",
            "nominations",
            "oscar_wins",
            "oscar_nominations",
        }
        urls = [
            "https://www.imdb.com/title/tt0120737/",
        ]

        results = Scraper(urls=urls, search_type=Movie.TYPE).handle()

        for url in urls:
            self.assertListEqual([], self.take_diff(attrs=expected_attrs, results=results[url]))

    def test__movie2(self):
        expected_attrs = {
            "imdb_genre",
            "imdb_director",
            "imdb_director_url",
            "run_time",
            "country",
            "language",
            "release_date",
            "imdb_title",
            "budget_amount",
            "budget_currency",
            "ww_amount",
            "ww_currency",
            "imdb_vote_count",
            "imdb_rate",
        }
        urls = [
            "https://www.imdb.com/title/tt7221896/",
        ]

        results = Scraper(urls=urls, search_type=Movie.TYPE).handle()

        for url in urls:
            self.assertListEqual([], self.take_diff(attrs=expected_attrs, results=results[url]))

    def test__movie3(self):
        expected_attrs = {
            "imdb_genre",
            "imdb_director",
            "imdb_director_url",
            "run_time",
            "imdb_popularity",
            "country",
            "language",
            "release_date",
            "imdb_title",
            "usa_ow_amount",
            "usa_ow_currency",
            "ww_amount",
            "ww_currency",
            "metacritic_score",
            "imdb_vote_count",
            "imdb_rate",
            "usa_ow_amount",
            "metacritic_score",
            "imdb_popularity",
            "usa_ow_currency",
            "wins",
            "nominations",
            "oscar_wins",
            "oscar_nominations",
        }
        urls = [
            "https://www.imdb.com/title/tt1877830/",
        ]

        results = Scraper(urls=urls, search_type=Movie.TYPE).handle()

        for url in urls:
            self.assertListEqual([], self.take_diff(attrs=expected_attrs, results=results[url]))

    def test__series1(self):
        expected_attrs = {
            "imdb_genre",
            "imdb_director",
            "imdb_director_url",
            "run_time",
            "country",
            "language",
            "release_date",
            "imdb_title",
            "is_active",
            "end_date",
            "imdb_vote_count",
            "imdb_rate",
            "episode_count",
            "season_count",
        }
        urls = [
            "https://www.imdb.com/title/tt2098220/",
        ]

        results = Scraper(urls=urls, search_type=Series.TYPE).handle()

        for url in urls:
            self.assertListEqual([], self.take_diff(attrs=expected_attrs, results=results[url]))

    def test__series2(self):
        expected_attrs = {
            "imdb_genre",
            "imdb_director",
            "imdb_director_url",
            "run_time",
            "country",
            "language",
            "release_date",
            "imdb_title",
            "is_active",
            "end_date",
            "imdb_vote_count",
            "imdb_rate",
            "episode_count",
            "season_count",
        }
        urls = ["https://www.imdb.com/title/tt0862622/"]

        results = Scraper(urls=urls, search_type=Series.TYPE).handle()

        for url in urls:
            self.assertListEqual([], self.take_diff(attrs=expected_attrs, results=results[url]))
