import re
from django.core.exceptions import ValidationError


def validate_robot_version_model(value):
    if not re.match("([A-Z0-9]{2})", value):
            raise ValidationError('Параметр должен содержать комбинацию двух букв и(или) цифр')
    return value
