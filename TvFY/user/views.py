from dj_rest_auth.views import LogoutView


class UserLogoutView(LogoutView):
    allowed_methods = "GET",
