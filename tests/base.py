import json
import os

from django.conf import settings
from django.test import TestCase
from rest_framework.test import APIClient

__all__ = ["BaseTestCase"]


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    @staticmethod
    def read_file(path, is_json=False):
        with open(os.path.join(settings.TEST_DATASET_DIR, path)) as f:
            file = f.read()
            if is_json:
                file = json.loads(file)
            return file

    @classmethod
    def is_subset(cls, attrs, results) -> bool:
        set_attrs = set(attrs)
        is_subset: bool = all(
            set_attrs.issubset(transaction) and set_attrs.issuperset(transaction)
            for transaction in results
        )
        return is_subset
