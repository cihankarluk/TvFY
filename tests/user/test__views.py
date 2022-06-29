from unittest.mock import patch

from allauth.account.adapter import DefaultAccountAdapter
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from tests.base import BaseTestCase
from TvFY.user.models import UserMovies


class UserSignupViewTestCase(BaseTestCase):
    signup_url = reverse("rest_register")

    def test__post(self):
        expected_attrs = {
            "access_token",
            "refresh_token",
            "user",
        }

        request_data = {
            "username": "test1",
            "email": "test@gmail.com",
            "password1": "ph420wwwW",
            "password2": "ph420wwwW",
        }
        response = self.client.post(self.signup_url, data=request_data)
        json_response = response.json()

        self.assertEqual(201, response.status_code)
        self.assertTrue(self.is_subset(attrs=expected_attrs, results=json_response))


class UserLoginViewTestCase(BaseTestCase):
    signup_url = reverse("rest_register")
    login_url = reverse("rest_login")

    def test__post(self):
        expected_attrs = {
            "access_token",
            "refresh_token",
            "user",
        }

        signup_request_data = {
            "username": "test1",
            "email": "test@gmail.com",
            "password1": "ph420wwwW",
            "password2": "ph420wwwW",
        }
        response = self.client.post(self.signup_url, data=signup_request_data)
        json_response = response.json()

        self.assertEqual(201, response.status_code)
        self.assertTrue(self.is_subset(attrs=expected_attrs, results=json_response))

        login_request_data = {
            "username": "test1",
            "password": "ph420wwwW",
        }
        response = self.client.post(self.login_url, data=login_request_data)
        json_response = response.json()

        self.assertEqual(200, response.status_code)
        self.assertTrue(self.is_subset(attrs=expected_attrs, results=json_response))


class UserLogoutViewTestCase(BaseTestCase):
    signup_url = reverse("rest_register")
    login_url = reverse("rest_login")
    logout_url = reverse("rest_logout")

    def test__post(self):
        expected_attrs = {
            "access_token",
            "refresh_token",
            "user",
        }

        signup_request_data = {
            "username": "test1",
            "email": "test@gmail.com",
            "password1": "ph420wwwW",
            "password2": "ph420wwwW",
        }
        response = self.client.post(self.signup_url, data=signup_request_data)
        json_response = response.json()

        self.assertEqual(201, response.status_code)
        self.assertTrue(self.is_subset(attrs=expected_attrs, results=json_response))

        login_request_data = {
            "username": "test1",
            "password": "ph420wwwW",
        }
        response = self.client.post(self.login_url, data=login_request_data)
        json_response = response.json()

        self.assertEqual(200, response.status_code)
        self.assertTrue(self.is_subset(attrs=expected_attrs, results=json_response))

        response = self.client.get(self.logout_url)
        json_response = response.json()

        self.assertEqual(200, response.status_code)
        self.assertDictEqual({"detail": "Successfully logged out."}, json_response)


class UserPasswordResetViewTestCase(BaseTestCase):
    signup_url = reverse("rest_register")
    password_reset_url = reverse("rest_password_reset")

    @patch.object(DefaultAccountAdapter, "send_mail")
    def test__post(self, mock_send_mail):
        expected_attrs = {
            "access_token",
            "refresh_token",
            "user",
        }

        signup_request_data = {
            "username": "test1",
            "email": "test@gmail.com",
            "password1": "ph420wwwW",
            "password2": "ph420wwwW",
        }
        response = self.client.post(self.signup_url, data=signup_request_data)
        json_response = response.json()

        self.assertEqual(201, response.status_code)
        self.assertTrue(self.is_subset(attrs=expected_attrs, results=json_response))

        reset_request_data = {
            "email": "test@gmail.com",
        }
        response = self.client.post(self.password_reset_url, data=reset_request_data)
        json_response = response.json()

        self.assertEqual(200, response.status_code)
        self.assertDictEqual({"detail": "Password reset e-mail has been sent."}, json_response)
        self.assertTrue(mock_send_mail.called)


class UserPasswordResetConfirmViewTestCase(BaseTestCase):
    signup_url = reverse("rest_register")
    login_url = reverse("rest_login")
    password_reset_url = reverse("rest_password_reset")

    @classmethod
    def get_password_reset_confirm_url(cls, uid, token):
        return reverse("password_reset_confirm", args=[uid, token])

    @patch.object(DefaultAccountAdapter, "send_mail")
    def test__post(self, mock_send_mail):
        expected_attrs = {
            "access_token",
            "refresh_token",
            "user",
        }
        signup_request_data = {
            "username": "test1",
            "email": "test@gmail.com",
            "password1": "ph420wwwW",
            "password2": "ph420wwwW",
        }
        response = self.client.post(self.signup_url, data=signup_request_data)
        json_response = response.json()
        self.assertEqual(201, response.status_code)
        self.assertTrue(self.is_subset(attrs=expected_attrs, results=json_response))

        reset_request_data = {
            "email": "test@gmail.com",
        }
        response = self.client.post(self.password_reset_url, data=reset_request_data)
        json_response = response.json()
        self.assertEqual(200, response.status_code)
        self.assertDictEqual({"detail": "Password reset e-mail has been sent."}, json_response)
        self.assertTrue(mock_send_mail.called)

        args, kwargs = mock_send_mail.call_args
        mail_data = args[-1]
        reset_url = mail_data["password_reset_url"].rsplit("/", 3)
        uid, token = reset_url[1], reset_url[2]
        reset_confirm_request_data = {
            "new_password1": "123qwe123TtQq",
            "new_password2": "123qwe123TtQq",
            "uid": uid,
            "token": token,
        }
        reset_confirm_url = self.get_password_reset_confirm_url(uid=uid, token=token)
        response = self.client.post(reset_confirm_url, data=reset_confirm_request_data)
        json_response = response.json()
        self.assertEqual(200, response.status_code)
        self.assertDictEqual(
            {"detail": "Password has been reset with the new password."},
            json_response,
        )

        #########
        # LOGIN #
        #########
        expected_response = {
            "code": 400,
            "type": "ValidationError",
            "reason": {"non_field_errors": ["Unable to log in with provided credentials."]},
        }
        login_request_data = {
            "username": "test1",
            "password": "ph420wwwW",
        }
        response = self.client.post(self.login_url, data=login_request_data)
        json_response = response.json()
        self.assertEqual(400, response.status_code)
        self.assertDictEqual(expected_response, json_response)

        #########
        # LOGIN #
        #########
        login_request_data = {
            "username": "test1",
            "password": "123qwe123TtQq",
        }
        response = self.client.post(self.login_url, data=login_request_data)
        json_response = response.json()
        self.assertEqual(200, response.status_code)
        self.assertTrue(self.is_subset(attrs=expected_attrs, results=json_response))


class UserPasswordChangeViewTestCase(BaseTestCase):
    signup_url = reverse("rest_register")
    login_url = reverse("rest_login")
    password_change_url = reverse("rest_password_change")

    def setUp(self) -> None:
        self.client = APIClient()

    def test__post(self):
        ##########
        # SIGNUP #
        ##########
        expected_attrs = {
            "access_token",
            "refresh_token",
            "user",
        }
        signup_request_data = {
            "username": "test1",
            "email": "test@gmail.com",
            "password1": "ph420wwwW",
            "password2": "ph420wwwW",
        }
        response = self.client.post(self.signup_url, data=signup_request_data)
        json_response = response.json()
        self.assertEqual(201, response.status_code)
        self.assertTrue(self.is_subset(attrs=expected_attrs, results=json_response))

        #########
        # LOGIN #
        #########
        login_request_data = {
            "username": "test1",
            "password": "ph420wwwW",
        }
        response = self.client.post(self.login_url, data=login_request_data)
        json_response = response.json()
        self.assertEqual(200, response.status_code)
        self.assertTrue(self.is_subset(attrs=expected_attrs, results=json_response))

        ###################
        # PASSWORD CHANGE #
        ###################
        password_change_request_data = {
            "new_password1": "123qwe123TtT",
            "new_password2": "123qwe123TtT",
        }
        response = self.client.post(self.password_change_url, data=password_change_request_data)
        json_response = response.json()
        self.assertEqual(200, response.status_code)
        self.assertDictEqual({"detail": "New password has been saved."}, json_response)

        #########
        # LOGIN #
        #########
        expected_response = {
            "code": 400,
            "type": "ValidationError",
            "reason": {"non_field_errors": ["Unable to log in with provided credentials."]},
        }
        login_request_data = {
            "username": "test1",
            "password": "ph420wwwW",
        }
        response = self.client.post(self.login_url, data=login_request_data)
        json_response = response.json()
        self.assertEqual(400, response.status_code)
        self.assertDictEqual(expected_response, json_response)

        #########
        # LOGIN #
        #########
        login_request_data = {
            "username": "test1",
            "password": "123qwe123TtT",
        }
        response = self.client.post(self.login_url, data=login_request_data)
        json_response = response.json()
        self.assertEqual(200, response.status_code)
        self.assertTrue(self.is_subset(attrs=expected_attrs, results=json_response))


class UserResendEmailVerificationViewTestCase(BaseTestCase):
    signup_url = reverse("rest_register")
    resend_email = reverse("rest_resend_email")

    @patch.object(DefaultAccountAdapter, "send_mail")
    def test__post(self, mock_send_mail):
        expected_attrs = {
            "access_token",
            "refresh_token",
            "user",
        }
        signup_request_data = {
            "username": "test1",
            "email": "test@gmail.com",
            "password1": "ph420wwwW",
            "password2": "ph420wwwW",
        }
        response = self.client.post(self.signup_url, data=signup_request_data)
        json_response = response.json()
        self.assertEqual(201, response.status_code)
        self.assertTrue(self.is_subset(attrs=expected_attrs, results=json_response))

        resend_request_data = {
            "email": "test@gmail.com",
        }
        response = self.client.post(self.resend_email, data=resend_request_data)
        json_response = response.json()
        self.assertEqual(200, response.status_code)
        self.assertDictEqual({"detail": "ok"}, json_response)
        self.assertTrue(mock_send_mail.called)


class UserVerifyEmailViewTestCase(BaseTestCase):
    signup_url = reverse("rest_register")
    resend_email = reverse("rest_resend_email")

    @classmethod
    def get_confirm_email_url(cls, key):
        return reverse("account_confirm_email", args=[key])

    @patch.object(DefaultAccountAdapter, "send_mail")
    def test__post(self, mock_send_mail):
        expected_attrs = {
            "access_token",
            "refresh_token",
            "user",
        }
        signup_request_data = {
            "username": "test1",
            "email": "test@gmail.com",
            "password1": "ph420wwwW",
            "password2": "ph420wwwW",
        }
        response = self.client.post(self.signup_url, data=signup_request_data)
        json_response = response.json()
        self.assertEqual(201, response.status_code)
        self.assertTrue(self.is_subset(attrs=expected_attrs, results=json_response))

        resend_request_data = {
            "email": "test@gmail.com",
        }
        response = self.client.post(self.resend_email, data=resend_request_data)
        json_response = response.json()
        self.assertEqual(200, response.status_code)
        self.assertDictEqual({"detail": "ok"}, json_response)
        self.assertTrue(mock_send_mail.called)

        args, kwargs = mock_send_mail.call_args
        mail_data = args[-1]
        key = mail_data["activate_url"].rsplit("/", 2)[1]
        confirm_mail_request_data = {
            "key": key,
        }
        response = self.client.post(self.get_confirm_email_url(key=key), data=confirm_mail_request_data)
        json_response = response.json()

        self.assertEqual(200, response.status_code)
        self.assertDictEqual({"detail": "ok"}, json_response)


class UserViewSetTestCase(BaseTestCase):
    movies_url = reverse("user-movies")
    series_url = reverse("user-series")

    def test__user_movies__post__create(self):
        expected_response = {
            "user",
            "username",
            "movie",
            "movie_title",
            "is_watched",
            "is_going_to_watch",
        }
        movie = self.create_movie(count=1)[0]

        request_data = {
            "tvfy_code": movie.tvfy_code,
            "is_watched": True,
            "is_going_to_watch": False,
        }
        response = self.client.post(self.movies_url, data=request_data)
        json_response = response.json()

        self.assertEqual(201, response.status_code)
        self.assertTrue(self.is_subset(attrs=expected_response, results=json_response))
        self.assertTrue(UserMovies.objects.filter(movie=movie).exists())

    def test__user_movies__post__movie_does_not_exists(self):
        expected_response = {
            "code": 404,
            "type": "MovieNotFoundError",
            "reason": "Movie not exists with x tvfy_code.",
        }

        request_data = {
            "tvfy_code": "x",
            "is_watched": True,
            "is_going_to_watch": False,
        }
        response = self.client.post(self.movies_url, data=request_data)
        json_response = response.json()

        self.assertEqual(404, response.status_code)
        self.assertDictEqual(expected_response, json_response)

    def test__user_movies__get(self):
        expected_attrs = {
            "max_imdb_rate",
            "min_imdb_rate",
            "avg_imdb_rate",
            "max_rt_audience_rate",
            "min_rt_audience_rate",
            "avg_rt_audience_rate",
            "max_rt_tomatometer_rate",
            "min_rt_tomatometer_rate",
            "avg_rt_tomatometer_rate",
            "max_metacritic_score",
            "min_metacritic_score",
            "avg_metacritic_score",
            "newest_movie_watched",
            "oldest_movie_watched",
            "time_spent",
            "genres",
            "countries",
            "languages",
            "watched_movies",
            "watch_list",
        }
        _ = self.create_user_movies(count=1)
        _ = self.create_user_movies(count=1, index_start=1, is_watched=False, is_going_to_watch=True)

        response = self.client.get(self.movies_url)
        json_response = response.json()

        self.assertEqual(200, response.status_code)
        self.assertTrue(self.is_subset(attrs=expected_attrs, results=json_response))

    def test__user_series__post(self):
        expected_attrs = {
            "user",
            "username",
            "series_title",
            "watched_season",
            "last_watched_episode",
            "is_watched",
            "is_going_to_watch",
        }
        series = self.create_series(count=1)[0]
        _ = self.create_season(count=1, season="1", series=series)[0]
        request_data = {
            "tvfy_code": series.tvfy_code,
            "watched_season": 1,
            "last_watched_episode": 10,
            "watched_past_seasons": False,
            "is_watched": True,
            "is_going_to_watch": False,
        }

        response = self.client.post(self.series_url, data=request_data)
        json_response = response.json()

        self.assertEqual(201, response.status_code)
        self.assertTrue(self.is_subset(attrs=expected_attrs, results=json_response))

    def test__user_series__get(self):
        expected_attrs = {
            "last_watched_episode",
            "series",
            "watched_seasons",
            "unwatched_seasons",
        }
        _ = self.create_user_series(count=1, last_watched_episode=10)[0]

        response = self.client.get(self.series_url)
        json_response = response.json()

        self.assertEqual(200, response.status_code)
        self.assertTrue(self.is_subset(attrs=expected_attrs, results=json_response))
