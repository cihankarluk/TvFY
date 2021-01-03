import re
from typing import Union

from TvFY.collector.helpers import SoupSelectionMixin
from TvFY.movies.models import Movie


class IMDBEpisodes(SoupSelectionMixin):
    url: str

    @staticmethod
    def get_imdb_vote_count(episode_data):
        vote_str = episode_data.find('span', class_='ipl-rating-star__total-votes').text
        vote_count = int("".join(re.findall(r'\d+', vote_str)))
        return vote_count

    @property
    def get_episodes(self) -> tuple:
        result = []
        css_selection = self.soup_selection(
            self.find_all, selection="info", tag="div"
        )
        for episode_data in css_selection:
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


class IMDBCast(SoupSelectionMixin):
    search_type: str

    @staticmethod
    def get_actor_name(cast_data: str) -> dict:
        first_name, *last_name = cast_data.split(" ")
        result = {"first_name": first_name, "last_name": " ".join(last_name)}
        return result

    @staticmethod
    def cast_information(cast_data: str) -> Union[bool, dict]:
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
        css_selection = self.soup_selection(
            self.find, selection="cast_list", tag="table"
        )
        for cast in css_selection.find_all("tr"):
            if character := cast.find('td', class_="character"):
                if self.search_type == Movie.type:
                    cast_information = {"character_name": character.a.text}
                else:
                    cast_information = self.cast_information(character.text.strip())
                if not cast_information:
                    continue

                actor = self.get_actor_name(cast.find("td", class_="").a.text.strip())
                actor.update(cast_information)
                results.append(actor)
        return "cast", results


class IMDBScrapper(IMDBEpisodes, IMDBCast):
    def __init__(self, soup, url, search_type):
        self.soup = soup
        self.url = url
        self.search_type = search_type

    @property
    def get_popularity(self) -> tuple:
        css_selection = self.soup_selection(
            self.find, selection="titleReviewBarSubItem", tag="div"
        )
        popularity = css_selection.span.text.split("(")
        result = "popularity", popularity[0].strip()
        return result

    @property
    def get_creator(self) -> tuple:
        css_selection = self.soup_selection(
            self.find, selection="credit_summary_item", tag="div"
        )
        result = "creator", css_selection.a.text.strip()
        return result

    @property
    def get_genre(self) -> tuple:
        css_selection = self.soup_selection(
            self.select_one, selection="#titleStoryLine > div:nth-child(10)"
        )
        genres = [genre.text.strip() for genre in css_selection.find_all('a')]
        result = "genres_imdb", genres
        return result

    @property
    def get_runtime(self) -> tuple:
        css_selection = self.soup_selection(
            self.find, tag="time"
        )
        result = "run_time", css_selection.text.strip()
        return result

    @property
    def get_language(self) -> tuple:
        language = self.soup_selection(
            self.select_one, selection='#titleDetails > div:nth-child(5) > a'
        )
        result = "language", language.text.strip()
        return result

    @property
    def get_country(self) -> tuple:
        self.soup.find("div", id="titleDetails")
        css_selection = self.soup_selection(
            self.select_one, selection="#titleDetails"
        )
        # TODO: titleDetails detayları alınacak
        result = "country", country.text.strip()
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
            ])
        return result
