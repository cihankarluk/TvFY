from urllib.parse import urljoin

from django.conf import settings

from TvFY.artist.models import Artist
from TvFY.genre.models import Genre
from TvFY.series.models import SeriesArtist, Series, Season, Episode


def get_urls(google_data: dict) -> list:
    urls = []
    if imdb_base := google_data.get("imdb_url"):
        urls.append(urljoin(imdb_base, settings.IMDB_CAST))
        urls.append(urljoin(imdb_base, settings.AWARDS))
        seasons_str = google_data.get("seasons", 0)
        # Add one due to python range
        seasons = int(seasons_str) + 1
        for season in range(1, seasons):
            season_base = urljoin(imdb_base, settings.IMDB_SEASON)
            urls.append(f"{season_base}{season}")
        urls.append(imdb_base)
    if rottentomatoes := google_data.get("rotten_tomatoes_url"):
        urls.append(rottentomatoes)
    return urls


class SaveData:
    def __init__(self, search_data):
        self.search_data = search_data

    @staticmethod
    def get_or_create_artist(cast):
        artist = Artist.objects.get_or_create(
            first_name=cast["first_name"],
            last_name=cast["last_name"]
        )
        return artist



    def save_data(self):
        # Out[1]: dict_keys(['', '', '',
        # '', '', '', '',
        # '1', '2', '', '', '', '',
        # '', '', '', '', '',
        # '', '', 'cast'])

        # TODO: country, language
        series_data = {
            "name": self.search_data["title"],
            "creator": self.search_data.get("creator"),
            "storyline": self.search_data.get("storyline"),
            "tv_network": self.search_data.get("network"),
            "rt_tomatometer": self.search_data.get("rt_tomatometer"),
            "rt_audience_rate": self.search_data.get("rt_audience_rate"),
            "release_date": self.search_data.get("release_date"),
            "run_time": self.search_data.get("run_time"),
            "imdb_popularity": self.search_data.get("popularity"),
            "wins": self.search_data.get("wins"),
            "nominations": self.search_data.get("nominations"),
            "is_active": self.search_data.get("is_active"),
            "imdb_url": self.search_data.get("imdb_url"),
            "rotten_tomatoes_url": self.search_data.get("rotten_tomatoes_url"),
            "end_date": self.search_data.get("end_date"),
            "imdb_rate": self.search_data.get("total_imdb_rate"),
            "imdb_vote_count": self.search_data.get("total_imdb_vote_count"),
            "rt_genre": self.search_data.get("rt_genre"),
            "imdb_genre": self.search_data.get("imdb_genre")
        }

        series = Series.objects.save_series(**series_data)

        for cast in self.search_data.get('casts', []):
            series = SeriesArtist.objects.create(
                character_name=cast["character_name"],
                episode_count=cast["episode_count"],
                start_acting=cast["start_acting"],
                end_acting=cast["end_acting"]
            )
            series.artists.add(self.get_or_create_artist(cast))

        for episode in self.search_data.get("episodes", []):
            Episode.objects.create(
                name=episode["name"],
                storyline=episode.get("storyline"),
                imdb_rate=episode.get("imdb_rate"),
                imdb_vote_count=episode.get("imdb_vote_count"),
                episode=episode.get("episode"),
            )
