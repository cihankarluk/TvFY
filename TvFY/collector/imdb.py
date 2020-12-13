from TvFY.core.helpers import error_report


class IMDBScrapper:
    def __init__(self, soup, url):
        self.soup = soup
        self.url = url
        self.error_objs = []

    @staticmethod
    def get_actor_name(cast_data):
        first_name, *last_name = cast_data[0].split(' ')
        result = {"first_name": first_name, "last_name": " ".join(last_name)}
        return result

    @staticmethod
    def get_series_name(cast_data):
        name = cast_data[~1]
        result = "series_name", name
        return result

    @staticmethod
    def get_acting_episode_count(cast_data):
        episode_count, _ = cast_data[~0].split(",")
        result = "episode_count", episode_count
        return result

    @staticmethod
    def get_acting_years(cast_data):
        _, years = cast_data[~0].split(",")
        years = years.split("-")
        result = {"start_acting": years[0], "end_acting": years[~0]}
        return result

    @error_report
    def soup_selection(self, css_selector: str) -> str:
        css_selection = self.soup.select_one(css_selector).text
        return css_selection

    @property
    def get_runtime(self) -> tuple:
        css_selector = "#titleDetails > div:nth-child(15) > time"
        run_time = self.soup_selection(css_selector=css_selector)
        result = "run_time", run_time.strip()
        return result

    @property
    def get_genre(self) -> tuple:
        css_selector = "#titleStoryLine > div:nth-child(10)"
        css_selection = self.soup.select_one(css_selector)
        genres = [genre.text.strip() for genre in css_selection.findAll('a')]
        result = "genres_imdb", genres
        return result

    @property
    def get_popularity(self) -> tuple:
        css_selector = "#title-overview-widget > div.plot_summary_wrapper > div.titleReviewBar > div:nth-child(3) > div.titleReviewBarSubItem > div:nth-child(2) > span"  # noqa
        css_selection = self.soup_selection(css_selector=css_selector)
        popularity, _ = css_selection.split("(")
        result = "popularity", popularity.strip()
        return result

    @property
    def get_episodes(self):
        return "cast", ""

    @property
    def get_cast(self):
        result = []
        css_selector = "#fullcredits_content > table.cast_list"
        css_selection = self.soup.select_one(css_selector)
        all_casts = [cast.text.strip()
                     for cast in css_selection.findAll("tr")
                     if cast.text.strip()]
        for cast in all_casts:
            data = {}
            cast_data = [c.strip() for c in cast.splitlines() if c.strip()]
            data.update([
                self.get_series_name(cast_data),
                self.get_acting_episode_count(cast_data),
            ])
            data.update(self.get_actor_name(cast_data))
            data.update(self.get_acting_years(cast_data))
            result.append(data)
        return "cast", result

    @property
    def get_creator(self) -> tuple:
        css_selector = "#title-overview-widget > div.plot_summary_wrapper > div.plot_summary > div:nth-child(2) > a"  # noqa
        creator = self.soup_selection(css_selector=css_selector)
        result = "creator", creator.strip()
        return result

    @property
    def get_language(self) -> tuple:
        css_selector = '#titleDetails > div:nth-child(5) > a'
        language = self.soup_selection(css_selector=css_selector)
        result = "language", language.strip()
        return result

    @property
    def get_country(self) -> tuple:
        css_selector = "#titleDetails > div:nth-child(4) > a"
        country = self.soup_selection(css_selector=css_selector)
        result = "country", country.strip()
        return result

    @property
    def get_errors(self) -> tuple:
        result = "errors", self.error_objs
        return result

    def run(self):
        result = {}
        if 'episodes' in self.url:
            result.update([
                self.get_episodes
            ])
        elif 'fullcredits' in self.url:
            result.update([
                self.get_cast
            ])
        else:
            result.update([
                self.get_runtime,
                self.get_genre,
                self.get_popularity,
                self.get_creator,
                self.get_language,
                self.get_country,
                self.get_errors
            ])
        return result
