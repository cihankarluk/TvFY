from itests.base import BaseTestCase


class GoogleScrapperTestCase(BaseTestCase):
    def setUp(self) -> None:
        self.expected_attrs = {
            "imdb_url",
            "rotten_tomatoes_url",
        }

    def test__the_dark_knight(self):
        result = self.get_google_result("the dark knight")

        self.assertTrue(self.is_subset(attrs=self.expected_attrs, results=[result]))

    def test__suicide_squad(self):
        result = self.get_google_result("suicide squad")

        self.assertTrue(self.is_subset(attrs=self.expected_attrs, results=[result]))

    def test__inception(self):
        result = self.get_google_result("inception")

        self.assertTrue(self.is_subset(attrs=self.expected_attrs, results=[result]))

    def test__the_boys(self):
        result = self.get_google_result("the boys")

        self.assertTrue(self.is_subset(attrs=self.expected_attrs, results=[result]))

    def test__hunter_x_hunter(self):
        expected_attrs = self.expected_attrs.copy()
        expected_attrs.remove("rotten_tomatoes_url")

        result = self.get_google_result("hunter x hunter")

        self.assertTrue(self.is_subset(attrs=expected_attrs, results=[result]))
