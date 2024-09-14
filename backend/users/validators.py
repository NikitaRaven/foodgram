import re

from django.core.exceptions import ValidationError

from .constants import INVALID_USERNAME


def validate_username(value):
    if not re.match(r'^[\w.@+-]+$', value):
        raise ValidationError(INVALID_USERNAME)
