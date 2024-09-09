from rest_framework.exceptions import ValidationError

from .constants import (
    COMMON_PASSWORDS, PASSWORD_USERNAME, PASSWORD_LENGTH, SHORT_PASSWORD,
    TOO_COMMON, ONLY_DIGITS
)


def validate_password(value, request, initial_data):
    username = initial_data.get('username') or request.user.username

    if username and username.lower() in value.lower():
        raise ValidationError(PASSWORD_USERNAME)

    if len(value) < PASSWORD_LENGTH:
        raise ValidationError(SHORT_PASSWORD)

    if value in COMMON_PASSWORDS:
        raise ValidationError(TOO_COMMON)

    if value.isdigit():
        raise ValidationError(ONLY_DIGITS)

    return value


class FirstPasswordMixin:
    def validate_password(self, value):
        request = self.context.get('request')
        return validate_password(value, request, self.initial_data)


class NewPasswordMixin:
    def validate_current_password(self, value):
        request = self.context.get('request')
        return validate_password(value, request, self.initial_data)

    def validate_new_password(self, value):
        request = self.context.get('request')
        return validate_password(value, request, self.initial_data)
