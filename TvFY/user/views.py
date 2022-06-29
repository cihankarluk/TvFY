from dj_rest_auth.app_settings import JWTSerializer
from dj_rest_auth.registration.views import RegisterView, ResendEmailVerificationView, VerifyEmailView
from dj_rest_auth.views import LogoutView, LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from drf_yasg import openapi
from drf_yasg.openapi import Schema
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from TvFY.user.serializers import UserMovieCreateOrUpdateSerializer, UserMovieGetMoviesSerializer, \
    UserMovieCreateOrUpdateRequestSerializer, UserSeriesCreateOrUpdateRequestSerializer, \
    UserSeriesCreateOrUpdateSerializer, UserSeriesGetSeriesSerializer
from TvFY.user.service import UserService


class UserSignupView(RegisterView):

    @swagger_auto_schema(responses={200: JWTSerializer})
    def post(self, request, *args, **kwargs):
        return super(UserSignupView, self).post(request, *args, **kwargs)


class UserLoginView(LoginView):

    @swagger_auto_schema(responses={200: JWTSerializer})
    def post(self, request, *args, **kwargs):
        return super(UserLoginView, self).post(request, *args, **kwargs)


class UserLogoutView(LogoutView):
    allowed_methods = "GET",


class UserPasswordResetView(PasswordResetView):

    @swagger_auto_schema(responses={200: Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'detail': openapi.Schema(
                type=openapi.TYPE_STRING,
                example="Password reset e-mail has been sent."
            )}
    )})
    def post(self, request, *args, **kwargs):
        return super(UserPasswordResetView, self).post(request, *args, **kwargs)


class UserPasswordResetConfirmView(PasswordResetConfirmView):

    @swagger_auto_schema(responses={200: Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'detail': openapi.Schema(
                type=openapi.TYPE_STRING,
                example="Password has been reset with the new password."
            )}
    )})
    def post(self, request, *args, **kwargs):
        return super(UserPasswordResetConfirmView, self).post(request, *args, **kwargs)


class UserPasswordChangeView(PasswordChangeView):

    @swagger_auto_schema(responses={200: Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'detail': openapi.Schema(
                type=openapi.TYPE_STRING,
                example="New password has been saved."
            )}
    )})
    def post(self, request, *args, **kwargs):
        return super(UserPasswordChangeView, self).post(request, *args, **kwargs)


class UserResendEmailVerificationView(ResendEmailVerificationView):

    @swagger_auto_schema(responses={200: Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'detail': openapi.Schema(
                type=openapi.TYPE_STRING,
                example="ok"
            )}
    )})
    def post(self, request, *args, **kwargs):
        return super(UserResendEmailVerificationView, self).post(request, *args, **kwargs)


class UserVerifyEmailView(VerifyEmailView):

    @swagger_auto_schema(responses={200: Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'detail': openapi.Schema(
                type=openapi.TYPE_STRING,
                example="ok"
            )}
    )})
    def post(self, request, *args, **kwargs):
        return super(UserVerifyEmailView, self).post(request, *args, **kwargs)


class UserViewSet(GenericViewSet):

    def get_serializer_class(self):
        if self.action == "user_movies":
            if self.request.method == "GET":
                return UserMovieGetMoviesSerializer
            elif self.request.method == "POST":
                return UserMovieCreateOrUpdateSerializer
        elif self.action == "user_series":
            if self.request.method == "GET":
                return UserSeriesGetSeriesSerializer
            elif self.request.method == "POST":
                return UserSeriesCreateOrUpdateSerializer

        return self.serializer_class

    @swagger_auto_schema(
        method="post",
        request_body=UserMovieCreateOrUpdateRequestSerializer
    )
    @action(
        methods=["get", "post"],
        detail=False,
        url_path="movies",
        url_name="movies",
    )
    def user_movies(self, request, *args, **kwargs):
        user = request.user
        if request.method == "GET":
            results = UserService.get_movies(user=user)

            serializer = self.get_serializer(results)

            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == "POST":
            user_movie = UserService.create_or_update_user_movie(user=user, request_data=request.data)

            serializer = self.get_serializer(user_movie)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        method="post",
        request_body=UserSeriesCreateOrUpdateRequestSerializer,
        responses={201: UserSeriesCreateOrUpdateSerializer(many=True)}
    )
    @action(
        methods=["get", "post"],
        detail=False,
        url_path="series",
        url_name="series",
    )
    def user_series(self, request, *args, **kwargs):
        user = request.user
        if request.method == "GET":
            results = UserService.get_user_series(user=user)

            serializer = self.get_serializer(results, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == "POST":
            user_series = UserService.create_or_update_user_series(user=user, request_data=request.data)

            serializer = self.get_serializer(user_series, many=True)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
