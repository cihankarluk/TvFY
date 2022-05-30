import logging

import djclick as click

from TvFY.actor.service import ActorService

logger = logging.getLogger(__name__)


@click.group()
def main():
    pass


@main.command()
def update_actors():
    logger.info("Started to update actors.")
    ActorService.scrap_and_update_actor()
    logger.info("Ended to update actors.")
