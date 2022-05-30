from TvFY.actor.service import ActorService
from itests.base import BaseTestCase


class ActorServiceItestCase(BaseTestCase):
    def setUp(self) -> None:
        super(ActorServiceItestCase, self).setUp()
        self.actor_cb = self.create_actor(imdb_url="https://www.imdb.com/name/nm0000288/")
        self.director_sm = self.create_actor(imdb_url="https://www.imdb.com/name/nm0532235/")
        self.director_ek = self.create_actor(imdb_url="https://www.imdb.com/name/nm0471392/", is_updated=True)

    def test__scrap_and_update_actor(self):
        ActorService.scrap_and_update_actor()

        self.assertIsNone(self.actor_cb.perks)
        self.assertIsNone(self.director_sm.perks)
        self.assertIsNone(self.director_ek.perks)
        self.actor_cb.refresh_from_db()
        self.director_sm.refresh_from_db()
        self.director_ek.refresh_from_db()
        self.assertIsNotNone(self.actor_cb.perks)
        self.assertIsNotNone(self.director_sm.perks)
        self.assertIsNone(self.director_ek.perks)
