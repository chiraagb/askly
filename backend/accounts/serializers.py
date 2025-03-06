from rest_framework import serializers
from common.utils import is_valid_email, is_valid_mobile
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthenticationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)

    def validate_username(self, value):
        if not is_valid_email(value) and not is_valid_mobile(value):
            raise serializers.ValidationError(
                f"{value} is not a valid email nor phone number eg:+9190..."
            )

        return value


class VerifyLoginOtpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    otp = serializers.IntegerField(required=True)

    def validate_username(self, value):
        if not is_valid_email(value) and not is_valid_mobile(value):
            raise serializers.ValidationError(
                f"{value} is not a valid email nor phone number"
            )
        return value

    def validate_otp(self, value):
        return value
