from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()

class SignUpSerializer(serializers.ModelSerializer):
    pass_confirm = serializers.CharField(max_length=128)
    
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'pass_confirm',
        )

    def validate(self, attrs):
        password = attrs.get('password')
        pass_confirm = attrs.get('pass_confirm')

        if len(password) < 6:
            error_short_pass = 'Password must have at least 6 characters'

            raise serializers.ValidationError(
                {
                    'password': error_short_pass,
                    'pass_confirm': error_short_pass,
                }
                )

        if password != pass_confirm:
            raise serializers.ValidationError('passwords must match!')
        return super().validate(attrs)
