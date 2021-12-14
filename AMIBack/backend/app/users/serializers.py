from django.conf import settings
from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists, get_username_max_length
from django.contrib.auth import authenticate, get_user_model
from django.http import HttpRequest
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, serializers
from backend.app.ChatBot.models import Client
from allauth.account import app_settings
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "email", "gsm"]


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]


class RegisterAPISerializer(serializers.Serializer):
    name = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    gsm = serializers.CharField(required=True, write_only=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                _("The two password fields didn't match."))
        return data

    def get_cleaned_data(self):
        return {
            'name': self.validated_data.get('name', ''),
            'gsm': self.validated_data.get('gsm', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        # setup_user_email(request, user, [])

        user.gsm = self.get_cleaned_data()['gsm']
        user.email = self.get_cleaned_data()['email']
        user.name = self.get_cleaned_data()['name']

        user.save()
        client = Client(user=user)
        client.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True, style={
                                     'input_type': 'password'})
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "id"]

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_email(self, email, password):
        if email and password:

            user = self.authenticate(email=email, password=password)
            return user
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        print("pass email", email, password, app_settings.AuthenticationMethod,
              app_settings.AUTHENTICATION_METHOD)
        user = None
        if 'allauth' in settings.INSTALLED_APPS:

            # Authentication with email

            if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
                user = self._validate_email(email, password)

        else:
            # Authentication without using allauth
            if email:
                try:
                    username = User.objects.get(
                        email__iexact=email).get_username()
                except User.DoesNotExist:
                    pass

            if username:
                user = self._validate_username_email(username, '', password)

        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user

        return attrs
