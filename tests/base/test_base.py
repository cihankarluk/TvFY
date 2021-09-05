import base64

from django.test import TestCase
from rest_framework.test import APIClient

from TvFY.account.models import Account


class BaseView(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        account = Account.objects.create(
            username="test_username",
            email="test_email",
        )
        account.set_password("test_pwd")
        account.save()
        auth = base64.b64encode(b"test_username:test_pwd").decode("ascii")
        self.headers = {"HTTP_AUTHORIZATION": f"Basic {auth}"}
