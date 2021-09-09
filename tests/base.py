import json
import os

from django.conf import settings
from django.test import TestCase

__all__ = ["BaseTestCase"]


class BaseTestCase(TestCase):
    @staticmethod
    def read_file(path, is_json=False):
        with open(os.path.join(settings.TEST_DATASET_DIR, path)) as f:
            file = f.read()
            if is_json:
                file = json.loads(file)
            return file
