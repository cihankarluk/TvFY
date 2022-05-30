import logging

import djclick as click

from TvFY.director.service import DirectorService

logger = logging.getLogger(__name__)


@click.group()
def main():
    pass


@main.command()
def update_directors():
    logger.info("Started to update directors.")
    DirectorService.scrap_and_update_director()
    logger.info("Ended to update directors.")
