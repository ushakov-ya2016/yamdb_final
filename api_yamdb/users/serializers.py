from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role',
        )
        model = User


class ConfirmationCodeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'confirmation_code')
        model = User


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email')
        model = User

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Имя пользователя не может быть "me"'
            )
        elif User.objects.filter(username=data.get('username')):
            if User.objects.get(
                username=data.get('username')
            ).email != data.get('email'):
                raise serializers.ValidationError('Такой username уже занят')
        elif User.objects.filter(email=data.get('email')):
            if User.objects.get(
                email=data.get('email')
            ).username != data.get('username'):
                raise serializers.ValidationError('Такой email уже занят')
        return data
