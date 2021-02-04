from rest_framework import generics, permissions

from TvFY.account.models import Account
from TvFY.account.serializers import AccountSerializer, CreateAccountSerializer


class UserSignUp(generics.CreateAPIView):
    serializer_class = CreateAccountSerializer
    permission_classes = [permissions.AllowAny]


class UserSingIn(generics.RetrieveAPIView):
    serializer_class = AccountSerializer

    def get_object(self):
        return Account.objects.get(username=self.request.user)
