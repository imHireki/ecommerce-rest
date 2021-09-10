"""
Serializers for the account app and Djoser package
"""
from djoser.serializers import UserSerializer


class UserProfileSerializer(UserSerializer):
    """ Overriding the Djoser 'users/me' serializer """
    class Meta(UserSerializer.Meta):
        """ Add first_name, last_name, cpf and birth_date """
        fields = (
            'id', 'username', 'first_name', 'last_name',
            'email', 'cpf', 'birth_date',
        )
