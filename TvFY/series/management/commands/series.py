import logging

import djclick as click

from TvFY.series.service import SeriesSeasonEpisodeService

logger = logging.getLogger(__name__)


@click.group()
def main():
    pass


@main.command()
def update_directors():
    logger.info("Started to update season episodes.")
    SeriesSeasonEpisodeService.scrap_and_update_episodes()
    logger.info("Ended to update season episodes.")
