from typing import Optional

from bs4 import BeautifulSoup

from TvFY.core.helpers import error_handler


class SoupSelectionMixin:
    select_one = "select_one"
    find = "find"
    find_all = "find_all"
    soup: BeautifulSoup

    def soup_selection(
        self, soup: BeautifulSoup, method: str, tag: str = None, **kwargs
    ) -> Optional[BeautifulSoup]:
        if method == self.select_one:
            css_selection = soup.select_one(**kwargs)
        elif method == self.find:
            css_selection = soup.find(tag, **kwargs)
        elif method == self.find_all:
            css_selection = soup.find_all(tag, **kwargs)
        else:
            css_selection = None
        return css_selection

    @staticmethod
    def get_name(cast_data: str) -> dict:
        first_name, *last_name = cast_data.split(" ")
        result = {"first_name": first_name, "last_name": " ".join(last_name)}
        return result
