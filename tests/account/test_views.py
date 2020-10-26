import base64
import json

from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy
from rest_framework.test import APIClient

from TvFY.account.models import Account


class UserSignUpTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse("sign_up")

    def test_user_sign_up_with_missing_field(self):
        request_data = {
            "username": "test",
            "email": "test@test.com"
        }

        expected_result = {
            'status_code': 400,
            'code': 'VALIDATION_ERROR',
            'error_message': {
                'password': ['This field is required.']
            }
        }

        response = self.client.post(
            self.url,
            data=json.dumps(request_data),
            content_type="application/json"
        )

        self.assertEqual(expected_result, response.json())

    def test_user_sign_up_with_correctly(self):
        request_data = {
            "username": "test",
            "password": "test_pwd",
            "email": "test@test.com"
        }

        response = self.client.post(
            self.url,
            data=json.dumps(request_data),
            content_type="application/json"
        )

        self.assertEqual(201, response.status_code)

    def test_user_sign_up_with_already_existing_username(self):
        mommy.make(Account, username="test")
        request_data = {
            "username": "test",
            "password": "test_pwd",
            "email": "test@test.com"
        }

        expected_result = {
            'status_code': 400,
            'code': 'USERNAME_ALREADY_EXISTS',
            'error_message': 'Please try another username.'
        }

        response = self.client.post(
            self.url,
            data=json.dumps(request_data),
            content_type="application/json"
        )

        self.assertEqual(expected_result, response.json())


class UserSignInTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse("sign_in")

    def test_user_sign_in_with_wrong_username(self):
        mommy.make(Account)
        auth = base64.b64encode(b'test:test').decode("ascii")
        headers = {
            'HTTP_AUTHORIZATION': f"Basic {auth}"
        }

        expected_result = {
            'status_code': 401,
            'code': 'VALIDATION_ERROR',
            'error_message': {
                'detail': 'Invalid username/password.'
            }
        }

        response = self.client.get(
            self.url,
            **headers
        )

        self.assertEqual(expected_result, response.json())

    def test_user_sign_in_success(self):
        user = Account.objects.create(
            username="test_username",
            email="test_email",
        )
        user.set_password("test_pwd")
        user.save()
        auth = base64.b64encode(b'test_username:test_pwd').decode("ascii")

        headers = {
            'HTTP_AUTHORIZATION': f"Basic {auth}"
        }

        expected_result = {
            'username': 'test_username',
            'email': 'test_email'
        }

        response = self.client.get(
            self.url,
            **headers
        )

        self.assertDictEqual(expected_result, response.json())
