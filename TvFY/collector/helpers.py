from bs4 import BeautifulSoup

from TvFY.core.helpers import error_handler


class SoupSelectionMixin:
    select_one = "select_one"
    find = "find"
    find_all = "find_all"
    soup: BeautifulSoup

    @error_handler
    def soup_selection(self, method: str, selection: str = None, tag: str = None):
        if method == self.select_one:
            css_selection = self.soup.select_one(selector=selection)
        elif method == self.find:
            css_selection = self.soup.find(tag, class_=selection)
        elif method == self.find_all:
            css_selection = self.soup.find_all(tag, class_=selection)
        else:
            css_selection = None
        return css_selection
