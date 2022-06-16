from TvFY.movies.models import Movie
from TvFY.search.service import SearchService
from TvFY.series.models import Series
from itests.base import BaseTestCase


class SearchViewSetTestCase(BaseTestCase):

    def test__scrap__series(self):
        expected_attrs = {
            "tvfy_code",
            "title",
            "storyline",
            "release_date",
            "end_date",
            "run_time",
            "is_active",
            "season_count",
            "wins",
            "nominations",
            "oscar_wins",
            "oscar_nominations",
            "tv_network",
            "imdb_rate",
            "imdb_vote_count",
            "imdb_popularity",
            "imdb_url",
            "rt_tomatometer_rate",
            "rt_audience_rate",
            "rotten_tomatoes_url",
            "metacritic_score",
            "creator",
            "genres",
            "country",
            "language",
        }
        valid_data = {"type": Series.TYPE}
        search_urls = [
            "https://www.imdb.com/title/tt1190634/",
            "https://www.imdb.com/title/tt1190634/fullcredits",
            "https://www.imdb.com/title/tt1190634/episodes?season=1"
        ]
        google_results = {"imdb_url": "https://www.imdb.com/title/tt1190634/"}

        result = SearchService.scrap(valid_data=valid_data, search_urls=search_urls, google_results=google_results)

        self.assertTrue(self.is_subset(attrs=expected_attrs, results=result.data))

    def test__create__movie(self):
        expected_attrs = {
            "tvfy_code",
            "title",
            "storyline",
            "release_date",
            "wins",
            "nominations",
            "oscar_wins",
            "oscar_nominations",
            "run_time",
            "imdb_rate",
            "imdb_vote_count",
            "imdb_popularity",
            "imdb_url",
            "rt_tomatometer_rate",
            "rt_tomatometer_count",
            "rt_audience_rate",
            "rt_audience_count",
            "rotten_tomatoes_url",
            "budget_amount",
            "budget_currency",
            "usa_ow_amount",
            "usa_ow_currency",
            "ww_amount",
            "ww_currency",
            "metacritic_score",
            "director",
            "genres",
            "country",
            "language",
        }

        valid_data = {"type": Movie.TYPE}
        search_urls = [
            "https://www.imdb.com/title/tt0120737/",
            "https://www.imdb.com/title/tt0120737/fullcredits",
        ]
        google_results = {"imdb_url": "https://www.imdb.com/title/tt0120737/"}

        result = SearchService.scrap(valid_data=valid_data, search_urls=search_urls, google_results=google_results)

        self.assertTrue(self.is_subset(attrs=expected_attrs, results=result.data))
