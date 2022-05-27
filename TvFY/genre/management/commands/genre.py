import djclick as click

from TvFY.genre.service import GenreService


@click.group()
def main():
    pass


@main.command()
def load_genres():
    GenreService.load_genres()
