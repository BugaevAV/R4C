import re
from django.core.exceptions import ValidationError



def validate_serial(value):
    if not re.match("([A-Z0-9]{2})", value):
            raise ValidationError('Параметр должен содержать комбинацию двух букв и(или) цифр')
    return value

def validate_creation_data(value):
        if not re.match("([0-9]{4})-([0-9]{2})-([0-9]{2})  ([0-9]{2}):([0-9]{2}):([0-9]{2})", value):
               raise ValidationError('Формат времени должен быть "YYYY-MM-DD hh:mm:ss"')
        return value
