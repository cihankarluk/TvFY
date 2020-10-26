from rest_framework import serializers

from TvFY.account.models import Account
from TvFY.core.exceptions import UsernameAlreadyExists
from TvFY.core.serializers import BaseSerializer


class CreateAccountSerializer(BaseSerializer, serializers.Serializer):
    def create(self, validated_data):
        try:
            Account.objects.get(username=validated_data["username"])
            raise UsernameAlreadyExists('Please try another username.')
        except Account.DoesNotExist:
            account = Account.objects.create(
                username=validated_data["username"],
                email=validated_data['email'],
            )
            account.set_password(validated_data["password"])
            account.save()
            return account

    def update(self, instance, validated_data):
        pass

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.CharField()


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "username", "email"
