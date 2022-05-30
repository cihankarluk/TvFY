from TvFY.director.service import DirectorService
from itests.base import BaseTestCase


class DirectorServiceItestCase(BaseTestCase):
    def setUp(self) -> None:
        super(DirectorServiceItestCase, self).setUp()
        self.director_cb = self.create_director(imdb_url="https://www.imdb.com/name/nm0000288/")
        self.director_cn = self.create_director(imdb_url="https://www.imdb.com/name/nm0634240/")
        self.director_ek = self.create_director(imdb_url="https://www.imdb.com/name/nm0471392/", is_updated=True)

    def test__scrap_and_update_director(self):
        DirectorService.scrap_and_update_director()

        self.assertIsNone(self.director_cb.perks)
        self.assertIsNone(self.director_cn.perks)
        self.assertIsNone(self.director_ek.perks)
        self.director_cb.refresh_from_db()
        self.director_cn.refresh_from_db()
        self.director_ek.refresh_from_db()
        self.assertIsNotNone(self.director_cb.perks)
        self.assertIsNotNone(self.director_cn.perks)
        self.assertIsNone(self.director_ek.perks)
