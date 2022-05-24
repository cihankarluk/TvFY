from itests.base import BaseTestCase
from TvFY.movies.models import Movie
from TvFY.series.models import Series


class IMDBEpisodesTestCase(BaseTestCase):
    def setUp(self) -> None:
        self.expected_attrs = {
            "name",
            "storyline",
            "imdb_rate",
            "imdb_vote_count",
            "episode",
            "release_date",
            "imdb_url",
        }

    def test__get_episodes__the_boys(self):
        url = "https://www.imdb.com/title/tt1190634/episodes?season=1"

        result = self.get_imdb_result(url=url, search_type=Series.TYPE)

        self.assertTrue(self.is_subset(attrs=self.expected_attrs, results=result[1]))

    def test__get_episodes__breaking_bad(self):
        url = "https://www.imdb.com/title/tt0903747/episodes?season=1"

        result = self.get_imdb_result(url=url, search_type=Series.TYPE)

        self.assertTrue(self.is_subset(attrs=self.expected_attrs, results=result[1]))

    def test__get_episodes__raised_by_wolves(self):
        url = "https://www.imdb.com/title/tt9170108/episodes?season=1"

        result = self.get_imdb_result(url=url, search_type=Series.TYPE)

        self.assertTrue(self.is_subset(attrs=self.expected_attrs, results=result[1]))

    def test__get_episodes__hunter_x_hunter(self):
        url = "https://www.imdb.com/title/tt2098220/episodes?season=1"

        result = self.get_imdb_result(url=url, search_type=Series.TYPE)

        self.assertTrue(self.is_subset(attrs=self.expected_attrs, results=result[1]))


class IMDBCastTestCase(BaseTestCase):
    def setUp(self) -> None:
        self.series_expected_attrs = {
            "first_name",
            "last_name",
            "character_name",
            "episode_count",
            "start_acting",
            "end_acting",
            "imdb_actor_url",
        }
        self.movies_expected_attrs = {
            "first_name",
            "last_name",
            "character_name",
            "imdb_actor_url",
        }

    def test__get_cast__the_boys(self):
        url = "https://www.imdb.com/title/tt1190634/fullcredits"

        result = self.get_imdb_result(url=url, search_type=Series.TYPE)

        self.assertTrue(self.is_subset(attrs=self.series_expected_attrs, results=result["cast"]))

    def test__get_cast__breaking_bad(self):
        url = "https://www.imdb.com/title/tt0903747/fullcredits"

        result = self.get_imdb_result(url=url, search_type=Series.TYPE)

        self.assertTrue(self.is_subset(attrs=self.series_expected_attrs, results=result["cast"]))

    def test__get_cast__raised_by_wolves(self):
        url = "https://www.imdb.com/title/tt9170108/fullcredits"

        result = self.get_imdb_result(url=url, search_type=Series.TYPE)

        self.assertTrue(self.is_subset(attrs=self.series_expected_attrs, results=result["cast"]))

    def test__get_cast__hunter_x_hunter(self):
        url = "https://www.imdb.com/title/tt2098220/fullcredits"

        result = self.get_imdb_result(url=url, search_type=Series.TYPE)

        self.assertTrue(self.is_subset(attrs=self.series_expected_attrs, results=result["cast"]))

    def test__get_cast__lotr(self):
        url = "https://www.imdb.com/title/tt0120737/fullcredits"

        result = self.get_imdb_result(url=url, search_type=Movie.TYPE)

        self.assertTrue(self.is_subset(attrs=self.movies_expected_attrs, results=result["cast"]))

    def test__get_cast__the_dark_knight(self):
        url = "https://www.imdb.com/title/tt0468569/fullcredits"

        result = self.get_imdb_result(url=url, search_type=Movie.TYPE)

        self.assertTrue(self.is_subset(attrs=self.movies_expected_attrs, results=result["cast"]))

    def test__get_cast__monsters(self):
        url = "https://www.imdb.com/title/tt0198781/fullcredits"

        result = self.get_imdb_result(url=url, search_type=Movie.TYPE)

        self.assertTrue(self.is_subset(attrs=self.movies_expected_attrs, results=result["cast"]))


class IMDBAwardsTestCase(BaseTestCase):
    def setUp(self) -> None:
        self.expected_attrs = {
            "wins",
            "nominations",
        }

    def test__get_awards__the_boys(self):
        url = "https://www.imdb.com/title/tt1190634/awards/"

        result = self.get_imdb_result(url=url, search_type=Series.TYPE)

        self.assertTrue(self.is_subset(attrs=self.expected_attrs, results=[result]))

    def test__get_awards__breaking_bad(self):
        url = "https://www.imdb.com/title/tt0903747/awards/"

        result = self.get_imdb_result(url=url, search_type=Series.TYPE)

        self.assertTrue(self.is_subset(attrs=self.expected_attrs, results=[result]))

    def test__get_awards__hunter_x_hunter(self):
        url = "https://www.imdb.com/title/tt2098220/awards/"

        result = self.get_imdb_result(url=url, search_type=Series.TYPE)

        self.assertTrue(self.is_subset(attrs=self.expected_attrs, results=[result]))

    def test__get_awards__lotr(self):
        url = "https://www.imdb.com/title/tt0120737/awards/"

        result = self.get_imdb_result(url=url, search_type=Movie.TYPE)

        self.assertTrue(self.is_subset(attrs=self.expected_attrs, results=[result]))

    def test__get_awards__the_dark_knight(self):
        url = "https://www.imdb.com/title/tt0468569/awards/"

        result = self.get_imdb_result(url=url, search_type=Movie.TYPE)

        self.assertTrue(self.is_subset(attrs=self.expected_attrs, results=[result]))

    def test__get_awards__monsters(self):
        url = "https://www.imdb.com/title/tt0198781/awards/"

        result = self.get_imdb_result(url=url, search_type=Movie.TYPE)

        self.assertTrue(self.is_subset(attrs=self.expected_attrs, results=[result]))


class IMDBPersonalDataTestCase(BaseTestCase):
    def setUp(self) -> None:
        self.expected_attrs = {
            "born_date",
            "born_at",
            "died_date",
            "died_at",
            "oscars",
            "oscar_nominations",
            "wins",
            "nominations",
            "perks",
        }

    def test__quentin_tarantino(self):
        url = "https://www.imdb.com/name/nm0000233/"

        result = self.get_imdb_result(url=url, search_type=Movie.TYPE)

        self.assertTrue(self.is_subset(attrs=self.expected_attrs, results=[result]))

    def test__alfred_hitchcock(self):
        url = "https://www.imdb.com/name/nm0000033/"

        result = self.get_imdb_result(url=url, search_type=Movie.TYPE)

        self.assertTrue(self.is_subset(attrs=self.expected_attrs, results=[result]))

    def test__tobey_maguire(self):
        url = "https://www.imdb.com/name/nm0001497/"

        result = self.get_imdb_result(url=url, search_type=Movie.TYPE)

        self.assertTrue(self.is_subset(attrs=self.expected_attrs, results=[result]))

    def test__anna_hathaway(self):
        url = "https://www.imdb.com/name/nm0004266/"

        result = self.get_imdb_result(url=url, search_type=Movie.TYPE)

        self.assertTrue(self.is_subset(attrs=self.expected_attrs, results=[result]))


class IMDBRatingTestCase(BaseTestCase):
    def test__get_total_vote__the_boys(self):
        url = "https://www.imdb.com/title/tt1190634/ratings/"

        result = self.get_imdb_result(url=url, search_type=Series.TYPE)

        self.assertTrue(result["imdb_vote_count"])

    def test__get_total_vote__hunter_x_hunter(self):
        url = "https://www.imdb.com/title/tt2098220/ratings/"

        result = self.get_imdb_result(url=url, search_type=Series.TYPE)

        self.assertTrue(result["imdb_vote_count"])

    def test__get_total_vote__lotr(self):
        url = "https://www.imdb.com/title/tt0120737/ratings/"

        result = self.get_imdb_result(url=url, search_type=Movie.TYPE)

        self.assertTrue(result["imdb_vote_count"])

    def test__get_average_rating__the_boys(self):
        url = "https://www.imdb.com/title/tt1190634/ratings/"

        result = self.get_imdb_result(url=url, search_type=Series.TYPE)

        self.assertTrue(result["imdb_rate"])

    def test__get_average_rating__hunter_x_hunter(self):
        url = "https://www.imdb.com/title/tt2098220/ratings/"

        result = self.get_imdb_result(url=url, search_type=Series.TYPE)

        self.assertTrue(result["imdb_rate"])

    def test__get_average_rating__lotr(self):
        url = "https://www.imdb.com/title/tt0120737/ratings/"

        result = self.get_imdb_result(url=url, search_type=Movie.TYPE)

        self.assertTrue(result["imdb_rate"])


class IMDBHomePageTestCase(BaseTestCase):
    def setUp(self) -> None:
        self.movie_expected_attrs = {
            "imdb_genre",
            "director",
            "imdb_director_url",
            "run_time",
            "imdb_popularity",
            "country",
            "language",
            "release_date",
            "title",
            "budget",
            "usa_opening_weekend",
            "ww_gross",
        }
        self.series_expected_attrs = {
            "imdb_genre",
            "director",
            "imdb_director_url",
            "run_time",
            "imdb_popularity",
            "country",
            "language",
            "release_date",
            "title",
            "get_is_active",
        }

    def test__movie__lotr(self):
        url = "https://www.imdb.com/title/tt0120737/"

        result = self.get_imdb_result(url=url, search_type=Movie.TYPE)

        self.is_subset(attrs=self.movie_expected_attrs, results=result)

    def test__movie__dark_knight(self):
        url = "https://www.imdb.com/title/tt0468569/"

        result = self.get_imdb_result(url=url, search_type=Movie.TYPE)

        self.is_subset(attrs=self.movie_expected_attrs, results=result)

    def test__movie__spirited_away(self):
        url = "https://www.imdb.com/title/tt0245429/"

        result = self.get_imdb_result(url=url, search_type=Movie.TYPE)

        self.is_subset(attrs=self.movie_expected_attrs, results=result)

    def test__series__the_boys(self):
        url = "https://www.imdb.com/title/tt1190634/"

        result = self.get_imdb_result(url=url, search_type=Series.TYPE)

        self.is_subset(attrs=self.series_expected_attrs, results=result)

    def test__series__hunter_x_hunter(self):
        url = "https://www.imdb.com/title/tt2098220"

        result = self.get_imdb_result(url=url, search_type=Series.TYPE)

        self.is_subset(attrs=self.series_expected_attrs, results=result)

    def test__series__avatar_the_last_airbender(self):
        url = "https://www.imdb.com/title/tt0417299/"

        result = self.get_imdb_result(url=url, search_type=Series.TYPE)

        self.is_subset(attrs=self.series_expected_attrs, results=result)
