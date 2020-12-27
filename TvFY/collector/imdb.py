import re
from typing import Union

import bs4


class IMDBEpisodes:
    soup: bs4.BeautifulSoup
    url: str

    @staticmethod
    def get_imdb_vote_count(episode_data):
        vote_str = episode_data.find('span', class_='ipl-rating-star__total-votes').text
        vote_count = int("".join(re.findall(r'\d+', vote_str)))
        return vote_count

    @property
    def get_episodes(self) -> tuple:
        result = []
        for episode_data in self.soup.find_all("div", class_="info"):
            data = {
                "name": episode_data.a['title'],
                "storyline": episode_data.find(
                    'div', class_='item_description').text.strip(),
                "imdb_rate": episode_data.find(
                    'span', class_='ipl-rating-star__rating').text,
                "imdb_vote_count": self.get_imdb_vote_count(episode_data),
                "episode": episode_data.meta['content'],
                "release_date": episode_data.find('div', class_='airdate').text.strip(),
                "season": self.url
            }
            result.append(data)
        return "episodes", result


class IMDBCast:
    soup: bs4.BeautifulSoup

    @staticmethod
    def get_actor_name(cast_data: str) -> dict:
        first_name, *last_name = cast_data.split(" ")
        result = {"first_name": first_name, "last_name": " ".join(last_name)}
        return result

    @staticmethod
    def get_character_name(cast_data: str) -> tuple:
        name = cast_data.split('\n')
        result = "character_name", name
        return result

    @staticmethod
    def get_series_information(cast_data: str) -> Union[bool, dict]:
        # info: '17 episodes, 2019-2022'
        character_name, info = cast_data.split('\n', 1)

        try:
            # 17, episodes, 2019-2022
            episode_count, _, years = info.split(" ")
        except ValueError:
            # '         / ...  \n                  17 episodes, 2019-2021'
            data = info.strip().split(" ")
            episode_count, years = data[-3], data[-1]

        if not episode_count:
            # Case for dummy data
            return False

        # years might be 2019 or 2019-2022
        years = years.split("-")
        result = {
            "character_name": character_name,
            "episode_count": episode_count,
            "start_acting": years[0],
            "end_acting": years[~0]
        }
        return result

    @property
    def get_cast(self):
        results = []
        css_selection = self.soup.find("table", class_="cast_list")
        for cast in css_selection.find_all("tr"):
            if character := cast.find('td', class_="character"):
                series_information = self.get_series_information(character.text.strip())
                if not series_information:
                    continue

                actor = self.get_actor_name(cast.find("td", class_="").a.text.strip())
                actor.update(series_information)
                results.append(actor)
        return "cast", results


class IMDBScrapper(IMDBEpisodes, IMDBCast):
    def __init__(self, soup, url):
        self.soup = soup
        self.url = url
        self.error_objs = []

    def soup_selection(self, css_selector: str, soup):
        css_selection = soup.select_one(selector=css_selector)
        return css_selection

    @property
    def get_runtime(self) -> tuple:
        css_selector = "#titleDetails > div:nth-child(15) > time"
        run_time = self.soup_selection(css_selector=css_selector, soup=self.soup)
        result = "run_time", run_time.text.strip()
        return result

    @property
    def get_genre(self) -> tuple:
        css_selector = "#titleStoryLine > div:nth-child(10)"
        css_selection = self.soup_selection(css_selector=css_selector, soup=self.soup)
        genres = [genre.text.strip() for genre in css_selection.findAll('a')]
        result = "genres_imdb", genres
        return result

    @property
    def get_popularity(self) -> tuple:
        css_selector = "#title-overview-widget > div.plot_summary_wrapper > div.titleReviewBar > div:nth-child(3) > div.titleReviewBarSubItem > div:nth-child(2) > span"  # noqa
        css_selection = self.soup_selection(css_selector=css_selector, soup=self.soup)
        popularity, _ = css_selection.text.split("(")
        result = "popularity", popularity.strip()
        return result

    @property
    def get_creator(self) -> tuple:
        css_selector = "#title-overview-widget > div.plot_summary_wrapper > div.plot_summary > div:nth-child(2) > a"  # noqa
        creator = self.soup_selection(css_selector=css_selector, soup=self.soup)
        result = "creator", creator.text.strip()
        return result

    @property
    def get_language(self) -> tuple:
        css_selector = '#titleDetails > div:nth-child(5) > a'
        language = self.soup_selection(css_selector=css_selector, soup=self.soup)
        result = "language", language.text.strip()
        return result

    @property
    def get_country(self) -> tuple:
        css_selector = "#titleDetails > div:nth-child(4) > a"
        country = self.soup_selection(css_selector=css_selector, soup=self.soup)
        result = "country", country.text.strip()
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
