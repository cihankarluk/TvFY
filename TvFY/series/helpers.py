from TvFY.series.service import SeasonEpisodeService, SeriesCastService, SeriesService


def save_data(search_data: dict):
    series_service = SeriesService(search_data=search_data)

    series = series_service.create_series

    cast_data = search_data.get("cast", [])
    series_cast_service = SeriesCastService(cast_data=cast_data, series=series)
    series_cast_service.create_series_cast()

    season_and_episodes = SeasonEpisodeService(search_data=search_data, series=series)
    season_and_episodes.create_season_and_episodes()
