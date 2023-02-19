"""Serializers for the account app"""

from django.contrib.auth import update_session_auth_hash

from rest_framework.serializers import CharField, ModelSerializer

from account.models import Account


class AccountSerializer(ModelSerializer):
    """Serializer for the ScorchUser object"""

    password = CharField(write_only=True, required=False)
    password_confirm = CharField(write_only=True, required=False)

    class Meta:
        model = Account
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_active',
            'last_login',
            'date_joined',
            'password',
            'password_confirm',
        )
        read_only_fields = (
            'last_login',
            'date_joined',
        )

    def create(self, validated_data):
        return Account.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        # TODO: what about all the other fields??
        instance.save()

        password = validated_data.get('password', None)
        password_confirm = validated_data.get('password_confirm', None)
        if password and password_confirm and password == password_confirm:
            instance.set_password(password)
            instance.save()

        update_session_auth_hash(self.context.get('request'), instance)
