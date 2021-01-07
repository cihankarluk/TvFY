from urllib.parse import urljoin

from django.conf import settings


def get_urls(google_data: dict) -> list:
    urls = []
    if imdb_base := google_data.get("imdb_url"):
        urls.append(urljoin(imdb_base, settings.IMDB_CAST))
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
