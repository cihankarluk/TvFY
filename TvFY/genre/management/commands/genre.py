import djclick as click

from TvFY.genre.service import GenreService


@click.group()
def main():
    pass


@main.command()
def create_genre_fixtures():
    GenreService.insert_genre_fixtures()
