class TomatoesScrapper:
    def __init__(self, soup):
        self.soup = soup

    @property
    def get_network(self) -> tuple:
        css_selector = "#detail_panel > div > table > tr > td:nth-child(2)"
        network = self.soup.select_one(css_selector).text
        result = "tv_network", network.strip()
        return result

    @property
    def get_average_tomatometer(self) -> tuple:
        css_selector = "#topSection > section > div.mop-ratings-wrap.score_panel.js-mop-ratings-wrap > section > section > div.mop-ratings-wrap__half.critic-score > h2 > span > span.mop-ratings-wrap__percentage"
        tomatometer = self.soup.select_one(css_selector).text
        result = "rotten_tomatoes_rate", tomatometer.strip()
        return result

    @property
    def get_average_audience_score(self) -> tuple:
        css_selector = "#topSection > section > div.mop-ratings-wrap.score_panel.js-mop-ratings-wrap > section > section > div.mop-ratings-wrap__half.audience-score > h2 > span > span.mop-ratings-wrap__percentage"
        audience_score = self.soup.select_one(css_selector).text
        result = "average_audience_score", audience_score.strip()
        return result

    @property
    def get_genre(self) -> tuple:
        css_selector = "#detail_panel > div > table > tr:nth-child(3) > td:nth-child(2)"
        genres = self.soup.select_one(css_selector).text
        genres = genres.strip().split("&")
        result = "genres_rotten", genres
        return result

    @property
    def get_series_info(self) -> tuple:
        css_selector = "#movieSynopsis"
        series_info = self.soup.select_one(css_selector).text
        result = "storyline", series_info.strip()
        return result

    def run(self):
        result = {}
        result.update([
            self.get_network,
            self.get_genre,
            self.get_series_info,
            self.get_average_audience_score,
            self.get_average_tomatometer
        ])
        return result
