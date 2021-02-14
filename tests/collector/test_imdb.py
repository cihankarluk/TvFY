from tests.collector.base_test import BaseTest
from TvFY.collector.base import Scrapper


class IMDBSeriesTestCase(BaseTest):
    def control_episodes(self, episodes):
        self.assertTrue(episodes[0]["storyline"])
        self.assertTrue(episodes[0]["imdb_rate"])
        self.assertTrue(episodes[0]["imdb_vote_count"])
        self.assertTrue(episodes[0]["episode"])
        self.assertTrue(episodes[0]["release_date"])
        self.assertTrue(episodes[0]["imdb_url"])

    def control_cast(self, cast):
        self.assertTrue(cast[0]["first_name"])
        self.assertTrue(cast[0]["last_name"])
        self.assertTrue(cast[0]["character_name"])
        self.assertTrue(cast[0]["episode_count"])
        self.assertTrue(cast[0]["start_acting"])
        self.assertTrue(cast[0]["end_acting"])

    def test_the_boys(self):
        urls = [
            "https://www.imdb.com/title/tt1190634/",
            "https://www.imdb.com/title/tt1190634/episodes?season=1",
            "https://www.imdb.com/title/tt1190634/episodes?season=2",
            "https://www.imdb.com/title/tt1190634/fullcredits",
            "https://www.imdb.com/title/tt1190634/awards",
        ]
        cls = Scrapper(urls=urls, search_type=self.series)
        result = cls.handle()

        cast = result.get("cast")
        season_1 = result.get(1)
        season_2 = result.get(2)

        self.assertTrue(cast)
        self.assertTrue(season_1)
        self.assertTrue(season_2)

        self.control_cast(cast)
        self.imdb_control_home_page(result)
        self.control_episodes(season_1)
        self.control_episodes(season_2)

        self.assertTrue(result["run_time"])
        self.assertTrue(result["is_active"])
        self.assertTrue(result["wins"])

    def test_breaking_bad(self):
        urls = [
            "https://www.imdb.com/title/tt0903747/",
            "https://www.imdb.com/title/tt0903747/episodes?season=1",
            "https://www.imdb.com/title/tt0903747/fullcredits",
            "https://www.imdb.com/title/tt0903747/awards",
        ]
        cls = Scrapper(urls=urls, search_type=self.series)
        result = cls.handle()

        cast = result.get("cast")
        season_1 = result.get(1)

        self.assertTrue(cast)
        self.assertTrue(season_1)

        self.control_cast(cast)
        self.imdb_control_home_page(result)
        self.control_episodes(season_1)

        self.assertTrue(result["run_time"])
        self.assertFalse(result["is_active"])
        self.assertTrue(result["wins"])

    def test_raised_by_wolves(self):
        urls = [
            "https://www.imdb.com/title/tt9170108/",
            "https://www.imdb.com/title/tt9170108/episodes?season=1",
            "https://www.imdb.com/title/tt9170108/fullcredits",
            "https://www.imdb.com/title/tt9170108/awards",
        ]
        cls = Scrapper(urls=urls, search_type=self.series)
        result = cls.handle()

        cast = result.get("cast")
        season_1 = result.get(1)

        self.assertTrue(cast)
        self.assertTrue(season_1)

        self.control_cast(cast)
        self.imdb_control_home_page(result)
        self.control_episodes(season_1)

        self.assertIsNone(result.get("run_time"))
        self.assertTrue(result["is_active"])
        self.assertFalse(result["wins"])

    def test_seven_deadly_sins(self):
        urls = [
            "https://www.imdb.com/title/tt3909224/",
            "https://www.imdb.com/title/tt3909224/episodes?season=1",
            "https://www.imdb.com/title/tt3909224/fullcredits",
            "https://www.imdb.com/title/tt3909224/awards",
        ]
        cls = Scrapper(urls=urls, search_type=self.series)
        result = cls.handle()

        cast = result.get("cast")
        season_1 = result.get(1)

        self.assertTrue(cast)
        self.assertTrue(season_1)

        self.control_cast(cast)
        self.imdb_control_home_page(result)
        self.control_episodes(season_1)

        self.assertTrue(result["run_time"])
        self.assertTrue(result["is_active"])
        self.assertFalse(result["wins"])


class IMDBMoviesTestCase(BaseTest):
    def control_cast(self, cast):
        self.assertTrue(cast[0]["first_name"])
        self.assertTrue(cast[0]["last_name"])
        self.assertTrue(cast[0]["character_name"])

    def test_lotr_fellowship_of_the_ring(self):
        urls = [
            "https://www.imdb.com/title/tt0120737/",
            "https://www.imdb.com/title/tt0120737/fullcredits",
            "https://www.imdb.com/title/tt0120737/awards",
        ]
        cls = Scrapper(urls=urls, search_type=self.movie)
        result = cls.handle()

        cast = result.get("cast")

        self.assertTrue(cast)
        self.control_cast(cast)
        self.imdb_control_home_page(result)

        self.assertTrue(result["budget"])
        self.assertTrue(result["run_time"])
        self.assertTrue(result["ww_gross"])
        self.assertTrue(result["usa_opening_weekend"])

    def test_the_dark_knight(self):
        urls = [
            "https://www.imdb.com/title/tt0468569/",
            "https://www.imdb.com/title/tt0468569/fullcredits",
            "https://www.imdb.com/title/tt0468569/awards",
        ]
        cls = Scrapper(urls=urls, search_type=self.movie)
        result = cls.handle()

        cast = result.get("cast")

        self.assertTrue(cast)
        self.control_cast(cast)
        self.imdb_control_home_page(result)

        self.assertTrue(result["budget"])
        self.assertTrue(result["run_time"])
        self.assertTrue(result["ww_gross"])
        self.assertTrue(result["usa_opening_weekend"])


class IMDBPersonalDataTestCase(BaseTest):
    def test_quentin_tarantino(self):
        urls = ["https://www.imdb.com/name/nm0000233/"]
        cls = Scrapper(urls=urls)
        result = cls.handle()

        self.imdb_control_personal_data(result)

        self.assertTrue("oscar")

    def test_alfred_hitchcock(self):
        urls = ["https://www.imdb.com/name/nm0000033/"]
        cls = Scrapper(urls=urls)
        result = cls.handle()

        self.imdb_control_personal_data(result)

        self.assertTrue("oscar_nominations")
