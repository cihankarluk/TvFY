from rest_framework import generics, permissions

from TvFY.account.serializers import AccountSerializer, CreateAccountSerializer


class UserSignUp(generics.CreateAPIView):
    serializer_class = CreateAccountSerializer
    permission_classes = [permissions.AllowAny]


class UserSingIn(generics.RetrieveAPIView):
    serializer_class = AccountSerializer

    def get_object(self):
        return self.request.account
