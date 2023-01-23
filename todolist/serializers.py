from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.db.models import Q
from todolist.models import Task, User
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils.translation import gettext_lazy as _


class TaskListSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)

    class Meta:
        model = Task
        fields = ('id', 'header', 'description', 'deadline', 'done')


class TaskCRUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class PasswordSetNewSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68)
    token = serializers.CharField(min_length=1)
    uidb64 = serializers.CharField(min_length=1)

    class Meta:
        model = User
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            new_password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            user_id = int(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(new_password)
            user.save()
            return user
        except Exception as error:
            raise AuthenticationFailed(error)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {'bad_token': _('Token is expired or invalid')}

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Для возможности получения токена по телефону или почте
class CustomTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=64, required=False)
    phone = serializers.CharField(max_length=20, required=False)
    password = serializers.CharField(max_length=65, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email', None)
        phone = attrs.get('phone', None)
        param_password = attrs.get('password', None)

        if not email and not phone:
            raise AuthenticationFailed("Invalid Credential, email or phone required. Try again")

        try:
            user = User.objects.get(Q(email=email) | Q(Q(phone__isnull=False) & Q(phone=phone)))
        except:
            raise AuthenticationFailed("Invalid Credential. Try again")

        if not user.check_password(param_password):
            raise AuthenticationFailed("Invalid Credential. Try again")

        token = get_tokens_for_user(user)

        return token
